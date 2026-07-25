"""Stable domain errors shared by CLI, API, workers, and the Web Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ErrorCode = Literal[
    "INPUT_INVALID",
    "RIGHTS_DECLARATION_REQUIRED",
    "ASSET_NOT_FOUND",
    "MEDIA_UNSUPPORTED",
    "MODEL_NOT_READY",
    "MODEL_CAPABILITY_MISMATCH",
    "MODEL_WEIGHTS_MISSING",
    "MODEL_LICENSE_NOT_ACCEPTED",
    "GPU_OUT_OF_MEMORY",
    "JOB_CANCELLED",
    "METRIC_UNAVAILABLE",
    "RENDER_FAILED",
    "PROJECT_CONFLICT",
    "INTERNAL_ERROR",
]


@dataclass
class DomainError(Exception):
    """An expected failure with a safe, stable error code."""

    code: ErrorCode
    message: str
    action: str | None = None
    details: dict[str, object] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
