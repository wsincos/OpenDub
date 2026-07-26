"""Validation for the case-level provenance contract used by the V2 gallery."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Literal, cast

ShowcaseContentStatus = Literal["archived_research_example", "replay", "blocked"]
_VALID_STATUSES = {"archived_research_example", "replay", "blocked"}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ShowcaseArtifact:
    role: Literal["ground_truth", "method_output"]
    path: str
    sha256: str
    method_id: str | None


@dataclass(frozen=True)
class ShowcaseCase:
    case_id: str
    display_name: str
    content_status: ShowcaseContentStatus
    timeline_eligible: bool
    artifacts: tuple[ShowcaseArtifact, ...]
    source_path: Path


def load_case_manifest(path: Path) -> ShowcaseCase:
    """Read a public showcase contract and reject unlicensed or overclaimed cases."""
    payload = _read_object(path)
    case_id = _required_string(payload, "case_id")
    display_name = _required_string(payload, "display_name")
    status = _required_string(payload, "content_status")
    if status not in _VALID_STATUSES:
        raise ValueError(f"content_status must be one of {sorted(_VALID_STATUSES)}")
    timeline_eligible = payload.get("timeline_eligible")
    if not isinstance(timeline_eligible, bool):
        raise ValueError("timeline_eligible must be a boolean")

    rights = _required_object(payload, "rights")
    if rights.get("redistribution") != "allowed-for-opendub-v2":
        raise ValueError("redistribution must be allowed-for-opendub-v2 for public media")
    _required_string(rights, "video")
    _required_string(rights, "reference_speech")

    authorization = _required_object(payload, "authorization_record")
    record_path = Path(_required_string(authorization, "record_path"))
    if record_path.is_absolute() or ".." in record_path.parts:
        raise ValueError("authorization_record.record_path must be repository-relative")
    _required_string(authorization, "approver_role")
    try:
        date.fromisoformat(_required_string(authorization, "approved_on"))
    except ValueError as error:
        raise ValueError("authorization_record.approved_on must be an ISO date") from error
    public_scope = authorization.get("public_scope")
    if not isinstance(public_scope, list) or not {"repository", "grant-application-video"}.issubset(
        set(public_scope)
    ):
        raise ValueError(
            "authorization_record.public_scope must include repository and grant-application-video"
        )

    contract = _required_object(payload, "input_contract")
    same_input = contract.get("same_input_across_methods")
    if not isinstance(same_input, bool):
        raise ValueError("input_contract.same_input_across_methods must be a boolean")
    _required_string(contract, "target_text_source")
    _required_string(contract, "ipa_source")
    if status == "replay" and not same_input:
        raise ValueError("Replay requires same_input_across_methods to be verified")
    if status == "replay" and not isinstance(contract.get("target_text"), str):
        raise ValueError("Replay requires a canonical target_text")

    provenance = _required_object(payload, "provenance")
    _required_string(provenance, "method_revision")
    _required_string(provenance, "result_origin")
    artifacts_value = payload.get("artifacts")
    if not isinstance(artifacts_value, list) or not artifacts_value:
        raise ValueError("artifacts must be a non-empty list")
    artifacts = tuple(_parse_artifact(item) for item in artifacts_value)
    if not any(item.role == "ground_truth" for item in artifacts):
        raise ValueError("artifacts must contain a ground_truth item")

    return ShowcaseCase(
        case_id=case_id,
        display_name=display_name,
        content_status=cast(ShowcaseContentStatus, status),
        timeline_eligible=timeline_eligible,
        artifacts=artifacts,
        source_path=path.resolve(),
    )


def _read_object(path: Path) -> dict[str, Any]:
    try:
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error.msg}") from error
    if not isinstance(payload, dict):
        raise ValueError("showcase manifest must be a JSON object")
    if payload.get("schema_version") != "opendub.showcase/v1":
        raise ValueError("unsupported showcase schema_version")
    return payload


def _parse_artifact(value: object) -> ShowcaseArtifact:
    if not isinstance(value, dict):
        raise ValueError("artifact must be an object")
    role = _required_string(value, "role")
    if role not in {"ground_truth", "method_output"}:
        raise ValueError("artifact role must be ground_truth or method_output")
    relative_path = _required_string(value, "path")
    pure_path = Path(relative_path)
    if pure_path.is_absolute() or ".." in pure_path.parts:
        raise ValueError("artifact path must be relative to the case output directory")
    digest = _required_string(value, "sha256")
    if not _SHA256.fullmatch(digest):
        raise ValueError("artifact sha256 must be a 64-character lowercase hexadecimal digest")
    method_id = value.get("method_id")
    if role == "method_output" and not isinstance(method_id, str):
        raise ValueError("method_output requires method_id")
    return ShowcaseArtifact(
        role=cast(Literal["ground_truth", "method_output"], role),
        path=relative_path,
        sha256=digest,
        method_id=cast(str | None, method_id),
    )


def _required_object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value
