from pathlib import Path

from opendub.application.evaluation_service import EvaluationService
from opendub.application.generation_service import GenerationService
from opendub.domain.assets import ConsentRecord, VoiceReference
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.testing import DeterministicTestAdapter
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


def test_evaluation_report_records_computed_and_unavailable_metrics(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    project = store.create("Evaluated project")
    reference_asset = ArtifactStore(tmp_path).ingest_bytes(
        project.id,
        kind="audio",
        display_name="authorized-reference.wav",
        data=b"test-only reference",
        extension="wav",
    )
    project = project.add_asset(reference_asset, expected_revision=project.revision)
    store.save(project, expected_revision=project.revision - 1)
    consent = ConsentRecord(material_source="self_recorded")
    reference = VoiceReference(
        asset_id=reference_asset.id,
        consent_id=consent.id,
        speaker_label="Test narrator",
    )
    project = project.add_voice_reference(consent, reference, expected_revision=project.revision)
    store.save(project, expected_revision=project.revision - 1)
    segment = DubbingSegment(
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="Evaluate this accepted take.",
        language="en",
        character_id=new_id(),
        voice_reference_id=reference.id,
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="opendub.test",
        status="ready",
    )
    project = project.add_segment(segment, expected_revision=project.revision)
    store.save(project, expected_revision=project.revision - 1)
    candidate = GenerationService(store, DeterministicTestAdapter()).generate_segment(
        project.id, segment.id, expected_revision=project.revision, seed=3
    )

    report = EvaluationService(store).evaluate_candidate(project.id, candidate.id)

    metrics = {metric.metric_id: metric for metric in report.metrics}
    assert report.json_path.is_file()
    assert report.markdown_path.is_file()
    assert metrics["sync.duration_error_ms"].value == 0
    assert metrics["audio.silence_ratio"].status == "ok"
    assert metrics["audio.clipping_ratio"].status == "ok"
    assert metrics["audio.integrated_lufs"].status == "unavailable"
    assert metrics["content.transcript_match"].status == "unavailable"
    assert metrics["speaker.similarity"].status == "unavailable"
    assert metrics["emotion.direction"].status == "unavailable"
    assert "DeterministicTestAdapter" not in report.markdown_path.read_text(encoding="utf-8")
