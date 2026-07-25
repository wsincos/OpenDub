"""Filesystem validation for static Method Atlas content."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from opendub.atlas.models import AtlasValidationError, MethodManifest


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: Path
    message: str


@dataclass(frozen=True)
class ValidationReport:
    issues: tuple[ValidationIssue, ...]
    method_count: int

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_content(root: Path) -> ValidationReport:
    """Validate every method manifest under a content root in deterministic order."""
    issues: list[ValidationIssue] = []
    method_count = 0
    for manifest_path in sorted((root / "methods").glob("*/method.json")):
        method_count += 1
        try:
            raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append(
                ValidationIssue(
                    "ATLAS_JSON_INVALID", manifest_path, "Method manifest is not valid JSON"
                )
            )
            continue
        try:
            MethodManifest.model_validate(raw)
        except AtlasValidationError as error:
            issues.append(
                ValidationIssue(str(error), manifest_path, "Method manifest failed validation")
            )
    return ValidationReport(tuple(issues), method_count)
