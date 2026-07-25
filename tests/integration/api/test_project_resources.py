import base64
from pathlib import Path

from fastapi.testclient import TestClient

from opendub.api.app import create_app
from opendub.domain.ids import new_id


def test_api_creates_authorized_reference_then_dubbing_segment(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    project = client.post("/api/v1/projects", json={"name": "Authorized film"}).json()

    asset = client.post(
        f"/api/v1/projects/{project['id']}/assets",
        json={
            "kind": "audio",
            "filename": "narrator.wav",
            "content_base64": base64.b64encode(b"local audio fixture").decode("ascii"),
            "expected_revision": project["revision"],
        },
    )
    assert asset.status_code == 201

    reference = client.post(
        f"/api/v1/projects/{project['id']}/voice-references",
        json={
            "asset_id": asset.json()["id"],
            "speaker_label": "Narrator",
            "material_source": "self_recorded",
            "expected_revision": asset.json()["project_revision"],
        },
    )
    assert reference.status_code == 201

    segment = client.post(
        f"/api/v1/projects/{project['id']}/segments",
        json={
            "start_us": 0,
            "end_us": 1_250_000,
            "text": "A verified local dubbing workflow.",
            "language": "en",
            "character_id": new_id(),
            "voice_reference_id": reference.json()["id"],
            "adapter_id": "galaxycong/emodubber",
            "emotion_label": "neutral",
            "emotion_intensity": 0.5,
            "expected_revision": reference.json()["project_revision"],
        },
    )

    assert segment.status_code == 201
    loaded = client.get(f"/api/v1/projects/{project['id']}").json()
    assert loaded["segments"][0]["text"] == "A verified local dubbing workflow."
    assert loaded["voice_references"][0]["speaker_label"] == "Narrator"


def test_api_rejects_stale_asset_upload_before_writing_a_project_reference(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    project = client.post("/api/v1/projects", json={"name": "Versioned film"}).json()
    payload = {
        "kind": "audio",
        "filename": "narrator.wav",
        "content_base64": base64.b64encode(b"local audio fixture").decode("ascii"),
        "expected_revision": project["revision"],
    }

    first = client.post(f"/api/v1/projects/{project['id']}/assets", json=payload)
    stale = client.post(f"/api/v1/projects/{project['id']}/assets", json=payload)

    assert first.status_code == 201
    assert stale.status_code == 409
    assert len(client.get(f"/api/v1/projects/{project['id']}").json()["assets"]) == 1


def test_api_serves_only_the_requested_local_project_asset(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    project = client.post("/api/v1/projects", json={"name": "Preview film"}).json()
    uploaded = client.post(
        f"/api/v1/projects/{project['id']}/assets",
        json={
            "kind": "video",
            "filename": "local-preview.mp4",
            "content_base64": base64.b64encode(b"local video fixture").decode("ascii"),
            "expected_revision": project["revision"],
        },
    ).json()

    response = client.get(f"/api/v1/projects/{project['id']}/assets/{uploaded['id']}")

    assert response.status_code == 200
    assert response.content == b"local video fixture"


def test_api_reports_missing_accepted_candidate_as_a_validation_error(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    project = client.post("/api/v1/projects", json={"name": "No accepted candidate"}).json()

    response = client.post(f"/api/v1/projects/{project['id']}/renders", json={})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INPUT_INVALID"


def test_api_imports_updates_and_removes_authorized_subtitle_segments(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    project = client.post("/api/v1/projects", json={"name": "Subtitle workflow"}).json()
    audio = client.post(
        f"/api/v1/projects/{project['id']}/assets",
        json={
            "kind": "audio",
            "filename": "narrator.wav",
            "content_base64": base64.b64encode(b"local audio fixture").decode("ascii"),
            "expected_revision": project["revision"],
        },
    ).json()
    reference = client.post(
        f"/api/v1/projects/{project['id']}/voice-references",
        json={
            "asset_id": audio["id"],
            "speaker_label": "Narrator",
            "material_source": "self_recorded",
            "expected_revision": audio["project_revision"],
        },
    ).json()
    subtitles = client.post(
        f"/api/v1/projects/{project['id']}/assets",
        json={
            "kind": "subtitle",
            "filename": "dialogue.srt",
            "content_base64": base64.b64encode(
                b"1\n00:00:00,000 --> 00:00:01,000\nFirst line.\n\n"
                b"2\n00:00:01,100 --> 00:00:02,000\nSecond line.\n"
            ).decode("ascii"),
            "expected_revision": reference["project_revision"],
        },
    ).json()

    imported = client.post(
        f"/api/v1/projects/{project['id']}/segments/import-subtitles",
        json={
            "asset_id": subtitles["id"],
            "language": "en",
            "voice_reference_id": reference["id"],
            "adapter_id": "galaxycong/emodubber",
            "expected_revision": subtitles["project_revision"],
        },
    )
    first_segment = imported.json()["segments"][0]
    edited = client.patch(
        f"/api/v1/projects/{project['id']}/segments/{first_segment['id']}",
        json={"text": "Edited line.", "expected_revision": imported.json()["revision"]},
    )
    removed = client.request(
        "DELETE",
        f"/api/v1/projects/{project['id']}/segments/{first_segment['id']}",
        json={"expected_revision": edited.json()["project_revision"]},
    )

    assert imported.status_code == 200
    assert len(imported.json()["segments"]) == 2
    assert edited.status_code == 200
    assert edited.json()["text"] == "Edited line."
    assert removed.status_code == 200
    assert len(removed.json()["segments"]) == 1
