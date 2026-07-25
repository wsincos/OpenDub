"""Dependency-light adapter protocols used by isolated model runtimes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from opendub.domain.segments import EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.capabilities import ModelCapabilities


@dataclass(frozen=True)
class DubbingRequest:
    """Fully materialized input passed from the pipeline to an adapter."""

    project_id: str
    segment_id: str
    segment_revision: int
    video_path: Path
    text: str
    language: str
    target_range: TimeRange
    voice_path: Path
    emotion: EmotionSpec
    seed: int
    options: dict[str, object]


@dataclass(frozen=True)
class AudioArtifact:
    """A normalized waveform output produced by an adapter or vocoder."""

    path: Path
    sample_rate: int
    channels: int
    duration_samples: int
    sha256: str


@dataclass(frozen=True)
class PreparedInput:
    """Deterministic prepared files and cache key for one model invocation."""

    work_dir: Path
    manifest_path: Path
    cache_key: str


class ModelAdapter(Protocol):
    """An implementation that can prepare and generate a standard audio artifact."""

    def capabilities(self) -> ModelCapabilities: ...

    def prepare(self, request: DubbingRequest, work_dir: Path) -> PreparedInput: ...

    def generate(self, prepared: PreparedInput) -> AudioArtifact: ...

    def cleanup(self) -> None: ...
