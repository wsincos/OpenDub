from pathlib import Path

from fastapi.testclient import TestClient

from opendub.api.app import create_app
from opendub.domain.assets import ConsentRecord, MediaAsset, VoiceReference
from opendub.domain.project import MethodSelection, Project
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.storage.project_store import ProjectStore


def test_preparation_api_records_authorized_inputs_and_exports_the_selected_method(
    tmp_path: Path,
) -> None:
    project = _project_waiting_for_input_authorizations()
    ProjectStore(tmp_path)._write_project(project)
    client = TestClient(create_app(workspace=tmp_path))
    video = project.assets[0]

    video_authorization = client.post(
        f"/api/v1/projects/{project.id}/input-authorizations",
        json={
            "input_kind": "video",
            "asset_id": video.id,
            "material_source": "self_recorded",
            "expected_revision": project.revision,
        },
    )
    text_authorization = client.post(
        f"/api/v1/projects/{project.id}/input-authorizations",
        json={
            "input_kind": "target_text",
            "material_source": "self_recorded",
            "expected_revision": video_authorization.json()["project_revision"],
        },
    )
    exported = client.post(f"/api/v1/projects/{project.id}/preparation-export")
    manifest = client.get(exported.json()["manifest_url"])

    assert video_authorization.status_code == 201
    assert video_authorization.json()["content_sha256"] == video.sha256
    assert text_authorization.status_code == 201
    assert exported.status_code == 200
    assert manifest.status_code == 200
    assert manifest.json()["method_selection"]["method_id"] == "galaxycong/hpmdubbing"
    assert manifest.json()["runtime"]["live_admitted"] is False


def _project_waiting_for_input_authorizations() -> Project:
    video = MediaAsset(
        kind="video",
        display_name="scene.mp4",
        relative_path="assets/scene.mp4",
        sha256="c" * 64,
        size_bytes=100,
        duration_us=2_000_000,
    )
    audio = MediaAsset(
        kind="audio",
        display_name="reference.wav",
        relative_path="assets/reference.wav",
        sha256="d" * 64,
        size_bytes=100,
        duration_us=1_000_000,
    )
    consent = ConsentRecord(material_source="self_recorded")
    reference = VoiceReference(
        asset_id=audio.id,
        consent_id=consent.id,
        speaker_label="Authorized performer",
    )
    segment = DubbingSegment(
        range=TimeRange(start_us=100_000, end_us=800_000),
        text="Approved target line.",
        language="en",
        character_id=reference.id,
        voice_reference_id=reference.id,
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="galaxycong/hpmdubbing",
        status="ready",
    )
    return Project(
        name="Authorized handoff",
        assets=(video, audio),
        consents=(consent,),
        voice_references=(reference,),
        method_selection=MethodSelection(
            method_id="galaxycong/hpmdubbing",
            method_manifest_version="method-manifest@f50dfa7",
            declared_need="Inspect hierarchical visual prosody.",
            required_inputs=("Video", "Target text", "Authorized reference speech"),
            optional_controls=(),
            runtime_status="unavailable",
            content_modes=("concept",),
            evidence_revision="f50dfa7",
        ),
        segments=(segment,),
    )
