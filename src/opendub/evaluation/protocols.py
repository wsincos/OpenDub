"""Metric plugin protocol and the standard project metric result model."""

from __future__ import annotations

from typing import Protocol

from opendub.domain.metrics import MetricResult


class MetricPlugin(Protocol):
    """A metric with explicit availability semantics."""

    def metric_id(self) -> str: ...

    def evaluate(self) -> MetricResult: ...
