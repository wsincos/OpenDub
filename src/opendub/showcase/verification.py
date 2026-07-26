"""Verification for public showcase bundles without decoding or rewriting media."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .manifest import load_case_manifest


def verify_public_case(case_path: Path, public_directory: Path, repo_root: Path) -> None:
    """Verify source media, public copies, derived features, and provenance hashes."""
    case = load_case_manifest(case_path)
    manifest = _read_object(case_path, "showcase manifest")
    provenance = _read_object(public_directory / "provenance.json", "showcase provenance")
    if provenance.get("schema_version") != "opendub.showcase-build/v1":
        raise ValueError("unsupported showcase provenance schema_version")
    if provenance.get("case_id") != case.case_id:
        raise ValueError("provenance case_id does not match case manifest")
    if provenance.get("content_status") != case.content_status:
        raise ValueError("provenance content_status does not match case manifest")
    records = _records_by_artifact(provenance)

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("showcase manifest artifacts must be a list")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("showcase manifest artifact must be an object")
        relative_path = _required_string(artifact, "path")
        expected_hash = _required_string(artifact, "sha256")
        source = _source_path(repo_root, artifact)
        if _sha256(source) != expected_hash:
            raise ValueError(f"source artifact SHA-256 mismatch: {source}")

        public_artifact = _relative_public_path(public_directory, relative_path)
        if not public_artifact.is_file():
            raise ValueError(f"public artifact is missing: {public_artifact}")
        if _sha256(public_artifact) != expected_hash:
            raise ValueError(f"public artifact SHA-256 mismatch: {public_artifact}")

        record = records.get(relative_path)
        if record is None:
            raise ValueError(f"provenance record is missing for artifact: {relative_path}")
        if record.get("artifact_sha256") != expected_hash:
            raise ValueError(f"provenance artifact SHA-256 mismatch: {relative_path}")
        _verify_feature(public_directory, record, case.case_id, expected_hash)
        if artifact.get("role") == "ground_truth":
            _verify_poster(public_directory, record)


def _records_by_artifact(provenance: dict[str, Any]) -> dict[str, dict[str, Any]]:
    produced = provenance.get("produced")
    if not isinstance(produced, list):
        raise ValueError("provenance produced must be a list")
    records: dict[str, dict[str, Any]] = {}
    for record in produced:
        if not isinstance(record, dict):
            raise ValueError("provenance record must be an object")
        path = _required_string(record, "artifact_path")
        if path in records:
            raise ValueError(f"duplicate provenance record: {path}")
        records[path] = record
    return records


def _verify_feature(
    public_directory: Path, record: dict[str, Any], case_id: str, source_hash: str
) -> None:
    feature_path = _relative_public_path(public_directory, _required_string(record, "feature_path"))
    if not feature_path.is_file():
        raise ValueError(f"feature JSON is missing: {feature_path}")
    if _sha256(feature_path) != _required_string(record, "feature_sha256"):
        raise ValueError(f"feature JSON SHA-256 mismatch: {feature_path}")
    feature = _read_object(feature_path, "feature JSON")
    if feature.get("schema_version") != "opendub.audio-features/v1":
        raise ValueError("unsupported audio feature schema_version")
    if feature.get("case_id") != case_id:
        raise ValueError("feature case_id does not match case manifest")
    artifact = feature.get("artifact")
    if not isinstance(artifact, dict) or artifact.get("source_sha256") != source_hash:
        raise ValueError(f"feature source SHA-256 mismatch: {feature_path}")

    mel_path = _relative_public_path(public_directory, _required_string(record, "mel_png_path"))
    if not mel_path.is_file():
        raise ValueError(f"mel PNG is missing: {mel_path}")
    if _sha256(mel_path) != _required_string(record, "mel_png_sha256"):
        raise ValueError(f"mel PNG SHA-256 mismatch: {mel_path}")


def _verify_poster(public_directory: Path, record: dict[str, Any]) -> None:
    poster_path = _relative_public_path(public_directory, _required_string(record, "poster_path"))
    if not poster_path.is_file():
        raise ValueError(f"poster is missing: {poster_path}")
    if _sha256(poster_path) != _required_string(record, "poster_sha256"):
        raise ValueError(f"poster SHA-256 mismatch: {poster_path}")


def _source_path(repo_root: Path, artifact: dict[str, Any]) -> Path:
    source_path = Path(_required_string(artifact, "source_path"))
    if source_path.is_absolute() or ".." in source_path.parts:
        raise ValueError("source_path must be repository-relative")
    source = repo_root / source_path
    if not source.is_file():
        raise ValueError(f"source media does not exist: {source}")
    return source


def _relative_public_path(public_directory: Path, value: str) -> Path:
    relative_path = Path(value)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError("public output path must be relative to the case directory")
    return public_directory / relative_path


def _read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value: Any = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"{label} is missing: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid {label}: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
