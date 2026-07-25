"""Timeline duration metrics with exact sample-to-microsecond conversion."""

from __future__ import annotations

from opendub.domain.metrics import MetricResult


def duration_error(
    *,
    target_duration_us: int,
    duration_samples: int,
    sample_rate: int,
) -> MetricResult:
    """Report generated duration minus target duration in signed milliseconds."""
    if target_duration_us <= 0 or duration_samples < 0 or sample_rate <= 0:
        return MetricResult(
            metric_id="sync.duration_error_ms",
            version="v1",
            status="failed",
            details={"reason": "invalid duration inputs"},
        )
    generated_us = round(duration_samples * 1_000_000 / sample_rate)
    return MetricResult(
        metric_id="sync.duration_error_ms",
        version="v1",
        status="ok",
        value=round((generated_us - target_duration_us) / 1_000, 3),
        unit="ms",
        higher_is_better=False,
        details={"target_duration_us": target_duration_us, "generated_duration_us": generated_us},
    )
