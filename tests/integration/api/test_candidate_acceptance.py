from pathlib import Path

from fastapi.testclient import TestClient

from opendub.api.app import create_app
from opendub.application.generation_service import GenerationService
from opendub.domain.assets import ConsentRecord, VoiceReference
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.testing import DeterministicTestAdapter
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


def test_api_accepts_current_candidate_with_optimistic_concurrency(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    project = store.create("Candidate review")
    asset = ArtifactStore(tmp_path).ingest_bytes(
        project.id,
        kind="audio",
        display_name="authorized.wav",
        data=b"test-only reference",
        extension="wav",
    )
    project = project.add_asset(asset, expected_revision=project.revision)
    store.save(project, expected_revision=1)
    consent = ConsentRecord(material_source="self_recorded")
    reference = VoiceReference(
        asset_id=asset.id,
        consent_id=consent.id,
        speaker_label="Test narrator",
    )
    project = project.add_voice_reference(consent, reference, expected_revision=project.revision)
    store.save(project, expected_revision=2)
    segment = DubbingSegment(
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="Review the candidate.",
        language="en",
        character_id=new_id(),
        voice_reference_id=reference.id,
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="opendub.test",
        status="ready",
    )
    project = project.add_segment(segment, expected_revision=project.revision)
    store.save(project, expected_revision=3)
    candidate = GenerationService(store, DeterministicTestAdapter()).generate_segment(
        project.id, segment.id, expected_revision=project.revision, seed=11
    )
    generated = store.load(project.id)

    response = TestClient(create_app(workspace=tmp_path)).post(
        f"/api/v1/projects/{project.id}/segments/{segment.id}/candidates/{candidate.id}/accept",
        json={"expected_revision": generated.revision},
    )

    assert response.status_code == 200
    assert response.json()["segments"][0]["accepted_candidate_id"] == candidate.id
    assert response.json()["segments"][0]["status"] == "accepted"

    rendered = TestClient(create_app(workspace=tmp_path)).post(
        f"/api/v1/projects/{project.id}/renders", json={"mix_mode": "remove"}
    )

    assert rendered.status_code == 201
    assert rendered.json()["dubbed_video_url"] is None
    assert rendered.json()["distribution_authorized"] is False
    audio = TestClient(create_app(workspace=tmp_path)).get(rendered.json()["dubbing_audio_url"])
    assert audio.status_code == 200
    assert audio.content[:4] == b"RIFF"

    evaluated = TestClient(create_app(workspace=tmp_path)).post(
        f"/api/v1/projects/{project.id}/candidates/{candidate.id}/evaluate"
    )

    assert evaluated.status_code == 200
    assert any(
        metric["metric_id"] == "sync.duration_error_ms" and metric["status"] == "ok"
        for metric in evaluated.json()["metrics"]
    )
    report = TestClient(create_app(workspace=tmp_path)).get(evaluated.json()["report_json_url"])
    assert report.status_code == 200
    assert report.json()["candidate_id"] == candidate.id
