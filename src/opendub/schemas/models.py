"""Pydantic-only contracts that are persisted beside generated candidate artifacts."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class RunManifest(BaseModel):
    """Reproducibility metadata captured for every generated candidate."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = "opendub.run/v1"
    id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    adapter_id: str = Field(min_length=1)
    adapter_version: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    weights_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    seed: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    input_hashes: dict[str, str] = {}
    options: dict[str, object] = {}
