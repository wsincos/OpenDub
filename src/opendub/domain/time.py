"""Integer time primitives for sample-accurate project timelines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeRange:
    """A positive half-open microsecond range: ``[start_us, end_us)``."""

    start_us: int
    end_us: int

    def __post_init__(self) -> None:
        if isinstance(self.start_us, bool) or isinstance(self.end_us, bool):
            raise ValueError("time boundaries must be integers")
        if self.start_us < 0:
            raise ValueError("start_us must be non-negative")
        if self.end_us <= self.start_us:
            raise ValueError("end_us must be greater than start_us")

    @property
    def duration_us(self) -> int:
        """Return the exact duration in integer microseconds."""
        return self.end_us - self.start_us
