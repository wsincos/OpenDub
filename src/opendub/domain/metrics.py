"""Portable metric results that distinguish unavailable from failed evaluation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

MetricStatus = Literal["ok", "not_applicable", "unavailable", "failed"]


class MetricResult(BaseModel):
    """The result of one metric plugin invocation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    metric_id: str
    version: str
    status: MetricStatus
    value: float | None = None
    unit: str | None = None
    higher_is_better: bool | None = None
    details: dict[str, object] = {}
