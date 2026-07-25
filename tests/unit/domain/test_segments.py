import pytest
from pydantic import ValidationError

from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec, SegmentStatus
from opendub.domain.time import TimeRange
from opendub.domain.transitions import transition_segment


def make_segment(*, status: SegmentStatus = "unconfigured") -> DubbingSegment:
    return DubbingSegment(
        id=new_id(),
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="OpenDub makes the emotion intentional.",
        language="en",
        character_id=new_id(),
        voice_reference_id=new_id(),
        emotion=EmotionSpec(label="happy", intensity=0.7),
        adapter_id="galaxycong/emodubber",
        status=status,
    )


def test_emotion_intensity_is_bounded() -> None:
    with pytest.raises(ValidationError):
        EmotionSpec(label="happy", intensity=1.01)


def test_unconfigured_segment_cannot_start_synthesizing() -> None:
    segment = make_segment()

    with pytest.raises(ValueError, match="unconfigured"):
        transition_segment(segment, "synthesizing")


def test_ready_segment_can_start_synthesizing() -> None:
    segment = make_segment(status="ready")

    transitioned = transition_segment(segment, "synthesizing")

    assert transitioned.status == "synthesizing"
    assert transitioned.revision == segment.revision + 1
