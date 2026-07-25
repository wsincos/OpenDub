"""Convert validated subtitle cues into ready-to-configure domain segments."""

from __future__ import annotations

from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.media.timeline import SubtitleCue


def segments_from_subtitles(
    cues: tuple[SubtitleCue, ...],
    *,
    language: str,
    character_id: str,
    voice_reference_id: str,
    adapter_id: str,
    emotion: EmotionSpec | None = None,
) -> tuple[DubbingSegment, ...]:
    """Create explicit, reviewable segment records from imported subtitle timing."""
    selected_emotion = emotion or EmotionSpec(label="neutral", intensity=0.5)
    return tuple(
        DubbingSegment(
            id=new_id(),
            range=cue.range,
            text=cue.text,
            language=language,
            character_id=character_id,
            voice_reference_id=voice_reference_id,
            emotion=selected_emotion,
            adapter_id=adapter_id,
            status="ready",
        )
        for cue in cues
    )
