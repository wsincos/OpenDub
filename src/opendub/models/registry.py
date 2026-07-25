"""Structured discovery of audited upstream model records."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

from opendub.models.audit import validate_upstream_registry

RegistryMaturity = Literal["planned", "experimental", "stable"]


class UpstreamSource(BaseModel):
    """Immutable origin evidence for an upstream implementation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    repository: str
    commit: str | None = None
    license: str | None = None


class UpstreamArtifact(BaseModel):
    """Checksum evidence for one downloadable upstream artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    role: str
    sha256: str


class UpstreamModel(BaseModel):
    """One discovery record, deliberately separate from a runnable adapter."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    display_name: str
    maturity: RegistryMaturity
    source: UpstreamSource
    artifacts: tuple[UpstreamArtifact, ...] = ()
    paper: str | None = None
    review: str | None = None

    @property
    def is_releasable(self) -> bool:
        """Return whether the registry permits this entry to be user-visible."""
        return self.maturity in {"experimental", "stable"}


class ModelRegistry:
    """Load only registry entries that meet their maturity-specific evidence gate."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def discover(self) -> tuple[UpstreamModel, ...]:
        """Validate and parse the upstream YAML registry."""
        result = validate_upstream_registry(self.path)
        if not result.is_valid:
            errors = "; ".join(result.errors)
            raise ValueError(f"invalid upstream registry: {errors}")
        document = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError("upstream registry must contain a mapping")
        entries = document.get("models")
        if not isinstance(entries, list):
            raise ValueError("upstream registry must contain a models list")
        return tuple(UpstreamModel.model_validate(entry) for entry in entries)
