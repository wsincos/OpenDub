"""Portable model manifests that bind capabilities to verified weight artifacts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from opendub.models.capabilities import ModelCapabilities
from opendub.models.weights import WeightArtifact


class AdapterManifest(BaseModel):
    """A complete, reproducible declaration for a runnable adapter release."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    model_id: str
    capabilities: ModelCapabilities
    artifacts: tuple[WeightArtifact, ...]
