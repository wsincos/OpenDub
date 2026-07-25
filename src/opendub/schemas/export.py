"""Deterministically export the public contracts used by OpenDub clients."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from opendub.domain.metrics import MetricResult
from opendub.domain.project import Project
from opendub.models.capabilities import ModelCapabilities
from opendub.schemas.models import RunManifest

_SCHEMA_MODELS: dict[str, type[BaseModel]] = {
    "project-v1.json": Project,
    "run-v1.json": RunManifest,
    "model-capabilities-v1.json": ModelCapabilities,
    "metrics-v1.json": MetricResult,
}


def export_schemas(destination: Path) -> dict[str, dict[str, object]]:
    """Write canonical JSON Schema files and return the documents for validation tests."""
    destination.mkdir(parents=True, exist_ok=True)
    exported: dict[str, dict[str, object]] = {}
    for filename, model in _SCHEMA_MODELS.items():
        schema = model.model_json_schema()
        destination_file = destination / filename
        destination_file.write_text(
            f"{json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True)}\n",
            encoding="utf-8",
        )
        exported[filename] = schema
    return exported
