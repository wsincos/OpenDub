"""A small explicit metric registry that prevents accidental metric substitution."""

from __future__ import annotations

from collections.abc import Mapping

from opendub.evaluation.protocols import MetricPlugin


class MetricRegistry:
    """Register metrics by stable identifiers and reject duplicate implementations."""

    def __init__(self) -> None:
        self._plugins: dict[str, MetricPlugin] = {}

    def register(self, plugin: MetricPlugin) -> None:
        metric_id = plugin.metric_id()
        if metric_id in self._plugins:
            raise ValueError(f"Metric is already registered: {metric_id}")
        self._plugins[metric_id] = plugin

    def plugins(self) -> Mapping[str, MetricPlugin]:
        """Expose registered metrics as a read-only mapping view."""
        return self._plugins
