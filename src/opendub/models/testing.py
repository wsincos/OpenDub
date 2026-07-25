"""Deterministic test-only audio generator; never registered as a production model."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]

from opendub.domain.segments import DubbingSegment
from opendub.models.protocols import AudioArtifact


class DeterministicTestAdapter:
    """Write a reproducible sine-wave fixture for pipeline integration tests only."""

    adapter_id = "opendub.test"
    adapter_version = "0.1.0"
    model_id = "opendub/deterministic-test"
    weights_sha256 = "0" * 64
    sample_rate = 24_000

    def generate(self, segment: DubbingSegment, destination: Path, *, seed: int) -> AudioArtifact:
        """Generate a quiet waveform precisely matching the segment duration."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        duration_samples = round(segment.range.duration_us * self.sample_rate / 1_000_000)
        timeline = np.arange(duration_samples, dtype=np.float32) / self.sample_rate
        frequency = 180.0 + (seed % 5) * 35.0
        waveform = 0.08 * np.sin(2 * np.pi * frequency * timeline)
        sf.write(destination, waveform, self.sample_rate, subtype="PCM_16")
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        return AudioArtifact(
            path=destination,
            sample_rate=self.sample_rate,
            channels=1,
            duration_samples=duration_samples,
            sha256=digest,
        )
