"""Low-resolution waveform summaries for the Web Studio timeline."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]


def build_waveform(path: Path, *, points: int = 1_000) -> tuple[float, ...]:
    """Return peak amplitudes in fixed buckets without exposing raw audio samples."""
    if points <= 0:
        raise ValueError("points must be positive")
    samples, _sample_rate = sf.read(path, dtype="float32", always_2d=True)
    values = np.max(np.abs(np.asarray(samples, dtype=np.float32)), axis=1)
    if values.size == 0:
        return ()
    chunks = np.array_split(values, min(points, values.size))
    return tuple(float(np.max(chunk)) for chunk in chunks)
