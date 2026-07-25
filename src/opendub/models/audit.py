"""Validate the provenance evidence required by the upstream model registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_RELEASABLE_MATURITY = frozenset({"experimental", "stable"})
_VALID_MATURITY = _RELEASABLE_MATURITY | {"planned"}


@dataclass(frozen=True)
class ValidationResult:
    """Errors accumulated while checking a registry document."""

    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Return whether all registry entries meet their evidence requirements."""
        return not self.errors


def validate_upstream_registry(path: Path) -> ValidationResult:
    """Validate immutable source and artifact evidence for releasable model entries.

    Planned entries may intentionally omit artifacts while their source, license, and
    runtime suitability are still being audited. Experimental and stable entries are
    user-visible capabilities and must therefore be pinned to a source commit and
    verified artifact checksums.
    """
    document = _load_registry(path)
    models = document.get("models")
    if not isinstance(models, list):
        return ValidationResult(("registry: models must be a list",))

    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, model in enumerate(models):
        if not isinstance(model, dict):
            errors.append(f"models[{index}]: entry must be a mapping")
            continue
        errors.extend(_validate_model(model, seen_ids, index))

    return ValidationResult(tuple(errors))


def _load_registry(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return {}
    return loaded


def _validate_model(model: dict[str, Any], seen_ids: set[str], index: int) -> list[str]:
    errors: list[str] = []
    model_id = _text(model.get("id"))
    label = model_id or f"models[{index}]"
    if not model_id:
        errors.append(f"{label}: id is required")
    elif model_id in seen_ids:
        errors.append(f"{label}: id must be unique")
    else:
        seen_ids.add(model_id)

    maturity = _text(model.get("maturity"))
    if maturity not in _VALID_MATURITY:
        errors.append(f"{label}: maturity must be planned, experimental, or stable")
        return errors
    if maturity not in _RELEASABLE_MATURITY:
        return errors

    source = model.get("source")
    if not isinstance(source, dict):
        return [*errors, f"{label}: source is required"]

    repository = _text(source.get("repository"))
    if not repository:
        errors.append(f"{label}: source.repository is required")
    elif not repository.startswith("https://"):
        errors.append(f"{label}: source.repository must use https")

    commit = _text(source.get("commit"))
    if not commit:
        errors.append(f"{label}: source.commit is required")
    elif not _COMMIT_PATTERN.fullmatch(commit):
        errors.append(f"{label}: source.commit must be a 40-character lowercase SHA")

    license_name = _text(source.get("license"))
    if not license_name:
        errors.append(f"{label}: source.license is required")
    elif license_name.lower() == "unknown":
        errors.append(f"{label}: source.license must be verified")

    artifacts = model.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{label}: artifacts are required")
        return errors
    for artifact_index, artifact in enumerate(artifacts):
        errors.extend(_validate_artifact(label, artifact_index, artifact))
    return errors


def _validate_artifact(label: str, index: int, artifact: Any) -> list[str]:
    if not isinstance(artifact, dict):
        return [f"{label}: artifacts[{index}] must be a mapping"]

    errors: list[str] = []
    if not _text(artifact.get("role")):
        errors.append(f"{label}: artifacts[{index}].role is required")
    checksum = _text(artifact.get("sha256"))
    if not checksum:
        errors.append(f"{label}: artifacts[{index}].sha256 is required")
    elif not _SHA256_PATTERN.fullmatch(checksum):
        errors.append(f"{label}: artifacts[{index}].sha256 must be a 64-character lowercase SHA")
    return errors


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""
