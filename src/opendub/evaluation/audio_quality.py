"""Simple deterministic waveform checks and truthful loudness availability reporting."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from opendub.domain.metrics import MetricResult


def silence_ratio(samples: ArrayLike, *, threshold: float = 1e-4) -> MetricResult:
    """Measure the fraction of samples below the configured absolute silence threshold."""
    values = np.asarray(samples, dtype=np.float32).reshape(-1)
    if values.size == 0:
        return _unavailable("audio.silence_ratio", "Audio is empty.")
    return MetricResult(
        metric_id="audio.silence_ratio",
        version="v1",
        status="ok",
        value=float(np.mean(np.abs(values) < threshold)),
        unit="ratio",
        higher_is_better=False,
        details={"threshold": threshold},
    )


def clipping_ratio(
    samples: ArrayLike,
    *,
    threshold: float = 0.999,
) -> MetricResult:
    """Measure the fraction of samples at or above the digital clipping threshold."""
    values = np.asarray(samples, dtype=np.float32).reshape(-1)
    if values.size == 0:
        return _unavailable("audio.clipping_ratio", "Audio is empty.")
    return MetricResult(
        metric_id="audio.clipping_ratio",
        version="v1",
        status="ok",
        value=float(np.mean(np.abs(values) >= threshold)),
        unit="ratio",
        higher_is_better=False,
        details={"threshold": threshold},
    )


def integrated_lufs(samples: ArrayLike, *, sample_rate: int) -> MetricResult:
    """Declare loudness unavailable until a standards-compliant backend is installed."""
    del samples, sample_rate
    return _unavailable(
        "audio.integrated_lufs",
        "No standards-compliant EBU R128 loudness backend is installed.",
    )


def _unavailable(metric_id: str, reason: str) -> MetricResult:
    return MetricResult(
        metric_id=metric_id,
        version="v1",
        status="unavailable",
        details={"reason": reason},
    )
