import pytest

from opendub.domain.candidates import Candidate
from opendub.domain.errors import DomainError
from opendub.domain.ids import new_id
from opendub.domain.project import Project
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange


def make_project() -> tuple[Project, DubbingSegment, Candidate]:
    segment = DubbingSegment(
        id=new_id(),
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="A controllable performance, grounded in the picture.",
        language="en",
        character_id=new_id(),
        voice_reference_id=new_id(),
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="galaxycong/emodubber",
        status="ready",
    )
    candidate = Candidate(
        id=new_id(),
        segment_id=segment.id,
        segment_revision=segment.revision,
        audio_asset_id=new_id(),
        adapter_id=segment.adapter_id,
        model_id="galaxycong/emodubber",
        seed=7,
    )
    project = Project(
        id=new_id(),
        name="Authorized demo",
        segments=(segment,),
        candidates=(candidate,),
    )
    return project, segment, candidate


def test_project_accepts_candidate_at_current_revision() -> None:
    project, segment, candidate = make_project()

    updated = project.accept_candidate(segment.id, candidate.id, expected_revision=project.revision)

    assert updated.revision == project.revision + 1
    assert updated.segments[0].accepted_candidate_id == candidate.id
    assert updated.segments[0].status == "accepted"


def test_project_rejects_stale_revision() -> None:
    project, segment, candidate = make_project()

    with pytest.raises(DomainError, match="PROJECT_CONFLICT"):
        project.accept_candidate(segment.id, candidate.id, expected_revision=project.revision - 1)
