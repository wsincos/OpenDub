"""Immutable generation candidates that can be compared and accepted."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from opendub.domain.ids import new_id, validate_uuid7


class Candidate(BaseModel):
    """One reproducible audio result for a particular segment revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    segment_id: str
    segment_revision: int = Field(ge=1)
    audio_asset_id: str
    adapter_id: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    seed: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revision: int = Field(default=1, ge=1)

    @field_validator("id", "segment_id", "audio_asset_id")
    @classmethod
    def validate_ids(cls, value: str) -> str:
        return validate_uuid7(value)
