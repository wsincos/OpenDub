"""Dubbing segment and emotion specifications."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from opendub.domain.ids import new_id, validate_uuid7
from opendub.domain.time import TimeRange

EmotionLabel = Literal[
    "neutral",
    "happy",
    "sad",
    "angry",
    "fearful",
    "surprised",
    "custom",
]
SegmentStatus = Literal[
    "unconfigured",
    "ready",
    "synthesizing",
    "generated",
    "accepted",
    "failed",
    "cancelled",
]


class EmotionSpec(BaseModel):
    """Declared emotional direction for a single spoken segment."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    label: EmotionLabel
    intensity: float = Field(ge=0.0, le=1.0)
    valence: float | None = Field(default=None, ge=-1.0, le=1.0)
    arousal: float | None = Field(default=None, ge=0.0, le=1.0)


class DubbingSegment(BaseModel):
    """One editable, versioned line of dialogue on the project timeline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    range: TimeRange
    text: str = Field(min_length=1, max_length=10_000)
    language: str = Field(min_length=2, max_length=35)
    character_id: str
    voice_reference_id: str
    emotion: EmotionSpec
    adapter_id: str = Field(min_length=1)
    status: SegmentStatus = "unconfigured"
    accepted_candidate_id: str | None = None
    revision: int = Field(default=1, ge=1)

    @field_validator("id", "character_id", "voice_reference_id", "accepted_candidate_id")
    @classmethod
    def validate_ids(cls, value: str | None) -> str | None:
        return validate_uuid7(value) if value is not None else None
