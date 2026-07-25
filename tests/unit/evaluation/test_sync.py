from opendub.evaluation.sync import duration_error


def test_duration_error_reports_signed_milliseconds() -> None:
    result = duration_error(
        target_duration_us=1_000_000,
        duration_samples=24_240,
        sample_rate=24_000,
    )

    assert result.metric_id == "sync.duration_error_ms"
    assert result.value == 10.0
    assert result.unit == "ms"
    assert result.higher_is_better is False
