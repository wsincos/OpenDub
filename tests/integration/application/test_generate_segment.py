from pathlib import Path

from opendub.application.generation_service import GenerationService
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.testing import DeterministicTestAdapter
from opendub.storage.project_store import ProjectStore


def test_generation_persists_candidate_audio_and_run_manifest(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    project = store.create("Authorized demo")
    segment = DubbingSegment(
        id=new_id(),
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="A verified local test candidate.",
        language="en",
        character_id=new_id(),
        voice_reference_id=new_id(),
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="opendub.test",
        status="ready",
    )
    project = project.add_segment(segment, expected_revision=project.revision)
    store.save(project, expected_revision=1)
    service = GenerationService(store, DeterministicTestAdapter())

    candidate = service.generate_segment(
        project.id,
        segment.id,
        expected_revision=project.revision,
        seed=7,
    )
    reloaded = store.load(project.id)
    candidate_dir = (
        tmp_path / "projects" / project.id / "segments" / segment.id / "candidates" / candidate.id
    )

    assert candidate.adapter_id == "opendub.test"
    assert candidate_dir.joinpath("audio.wav").is_file()
    assert candidate_dir.joinpath("run.json").is_file()
    assert reloaded.segments[0].status == "generated"
    assert reloaded.segments[0].revision == candidate.segment_revision
    assert reloaded.candidates == (candidate,)
