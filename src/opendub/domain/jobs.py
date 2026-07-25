"""Persistent local job state and structured progress events."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from opendub.domain.ids import new_id, validate_uuid7

JobKind = Literal[
    "media.analyze",
    "media.proxy",
    "segment.generate",
    "segment.evaluate",
    "project.generate",
    "project.evaluate",
    "project.render",
    "system.download_model",
]
JobStatus = Literal[
    "queued",
    "preparing",
    "running",
    "finalizing",
    "succeeded",
    "cancelling",
    "cancelled",
    "failed",
    "interrupted",
]


class Job(BaseModel):
    """A versioned unit of local pipeline work."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    project_id: str
    kind: JobKind
    status: JobStatus = "queued"
    segment_id: str | None = None
    segment_revision: int | None = Field(default=None, ge=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revision: int = Field(default=1, ge=1)

    @field_validator("id", "project_id", "segment_id")
    @classmethod
    def validate_ids(cls, value: str | None) -> str | None:
        return validate_uuid7(value) if value is not None else None
