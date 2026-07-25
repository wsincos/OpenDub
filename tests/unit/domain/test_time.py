import pytest

from opendub.domain.time import TimeRange


def test_time_range_uses_positive_microsecond_window() -> None:
    time_range = TimeRange(start_us=1_000_000, end_us=2_250_000)

    assert time_range.duration_us == 1_250_000


@pytest.mark.parametrize(
    ("start_us", "end_us"),
    [(-1, 1), (0, 0), (100, 99)],
)
def test_time_range_rejects_invalid_boundaries(start_us: int, end_us: int) -> None:
    with pytest.raises(ValueError):
        TimeRange(start_us=start_us, end_us=end_us)
