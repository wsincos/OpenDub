"""Typed descriptions of cacheable local generation pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PipelineStageName = Literal["prepare", "generate", "postprocess", "evaluate"]


@dataclass(frozen=True)
class PipelineStage:
    """One deterministic stage and the complete cache key for its declared inputs."""

    name: PipelineStageName
    cache_key: str

    def __post_init__(self) -> None:
        if len(self.cache_key) != 64 or any(
            character not in "0123456789abcdef" for character in self.cache_key
        ):
            raise ValueError("cache_key must be a lowercase SHA-256 hex digest")
