"""Serializable job and event records for the local execution ledger."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from opendub.domain.ids import new_id

JobStatus = Literal[
    "queued",
    "running",
    "succeeded",
    "failed",
    "cancelling",
    "cancelled",
    "interrupted",
]
JobResource = Literal["cpu", "gpu"]


class JobRecord(BaseModel):
    """One local operation with a state that survives process restarts."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    project_id: str
    kind: str
    resource: JobResource = "cpu"
    status: JobStatus = "queued"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revision: int = Field(default=1, ge=1)


class JobEvent(BaseModel):
    """A monotonically ordered progress event for one persisted job."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: int = Field(ge=1)
    job_id: str
    time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    stage: str
    message: str
    progress: float | None = Field(default=None, ge=0.0, le=1.0)
    level: Literal["info", "warning", "error"] = "info"
    details: dict[str, object] = {}
