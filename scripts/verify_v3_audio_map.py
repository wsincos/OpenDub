#!/usr/bin/env python3
"""Verify that every V3 archived film clip uses its visible artifact's audio."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "opendub.v3-source-audio-map/v1"
NARRATION_SOURCE = "docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4#a:0"
EXPECTED_RANGES = (
    "00:00-00:14",
    "00:14-00:28",
    "00:28-00:50",
    "00:50-01:07",
    "01:23-01:38",
    "01:38-01:50",
)
ARTIFACT_LABELS = {
    "gt.mp4": "Ground truth",
    "hpmdubbing.mp4": "HPMDubbing",
    "styledubber.mp4": "StyleDubber",
    "emodubber.mp4": "EmoDubber",
}
CASE_IDS = ("human-0", "animation-1")
EXPECTED_PAIRS = {(case_id, artifact) for case_id in CASE_IDS for artifact in ARTIFACT_LABELS}


def _as_object(value: object, label: str, issues: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        issues.append(f"{label} must be an object")
        return {}
    return value


def _as_list(value: object, label: str, issues: list[str]) -> list[Any]:
    if not isinstance(value, list):
        issues.append(f"{label} must be a list")
        return []
    return value


def _string(record: dict[str, Any], key: str, label: str, issues: list[str]) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        issues.append(f"{label}.{key} must be a non-empty string")
        return ""
    return value


def _path_from_stream(source: str) -> str:
    return source.split("#", maxsplit=1)[0]


def _check_existing(root: Path, source: str, label: str, issues: list[str]) -> None:
    if source and not (root / _path_from_stream(source)).is_file():
        issues.append(f"{label} is missing: {_path_from_stream(source)}")


def verify_audio_map(path: Path, root: Path, require_captures: bool) -> list[str]:
    """Return contract violations for a V3 source-audio map, without raising on bad input."""
    issues: list[str] = []
    try:
        payload: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot read source-audio map: {error}"]

    root_record = _as_object(payload, "source-audio map", issues)
    if root_record.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"schema_version must equal {SCHEMA_VERSION}")

    narration_source = _string(root_record, "narration_source", "source-audio map", issues)
    if narration_source != NARRATION_SOURCE:
        issues.append("narration_source must reference the approved V1 MP4 audio stream")
    _check_existing(root, narration_source, "narration source", issues)

    narration_clips = _as_list(root_record.get("narration_clips"), "narration_clips", issues)
    if len(narration_clips) != 6:
        issues.append("narration_clips must contain exactly six V1 narration records")
    ranges: list[str] = []
    for index, raw_record in enumerate(narration_clips):
        record = _as_object(raw_record, f"narration_clips[{index}]", issues)
        _string(record, "clip_id", f"narration_clips[{index}]", issues)
        ranges.append(_string(record, "source_range", f"narration_clips[{index}]", issues))
    if tuple(ranges) != EXPECTED_RANGES:
        issues.append("narration_clips must use the approved ordered V1 source ranges")

    archive_clips = _as_list(root_record.get("archive_clips"), "archive_clips", issues)
    if len(archive_clips) != 8:
        issues.append("archive_clips must contain exactly eight case/artifact records")

    seen_pairs: set[tuple[str, str]] = set()
    for index, raw_record in enumerate(archive_clips):
        record = _as_object(raw_record, f"archive_clips[{index}]", issues)
        label = f"archive_clips[{index}]"
        clip_id = _string(record, "clip_id", label, issues)
        case_id = _string(record, "case_id", label, issues)
        artifact_path = _string(record, "artifact_path", label, issues)
        visual_source = _string(record, "visual_source", label, issues)
        audio_source = _string(record, "audio_source", label, issues)
        in_frame_label = _string(record, "in_frame_label", label, issues)
        content_status = _string(record, "content_status", label, issues)
        if case_id not in CASE_IDS:
            issues.append(f"{label} has unsupported case_id: {case_id}")
        if artifact_path not in ARTIFACT_LABELS:
            issues.append(f"{label} has unsupported artifact_path: {artifact_path}")
        pair = (case_id, artifact_path)
        if pair in seen_pairs:
            issues.append(f"{label} duplicates case/artifact pair: {case_id}/{artifact_path}")
        seen_pairs.add(pair)
        expected_audio = f"apps/web/public/showcases/v2/{case_id}/{artifact_path}#a:0"
        if audio_source != expected_audio:
            issues.append(f"{label} must use the visible artifact audio: {expected_audio}")
        expected_label = f"AUDIBLE: {ARTIFACT_LABELS.get(artifact_path, 'unknown')}"
        if in_frame_label != expected_label:
            issues.append(f"{label} in_frame_label must equal {expected_label}")
        if content_status != "archived_research_example":
            issues.append(f"{label} content_status must be archived_research_example")
        if not clip_id.startswith(f"{case_id}-"):
            issues.append(f"{label} clip_id must begin with its case_id")
        _check_existing(root, audio_source, f"{label} audio source", issues)
        if require_captures and visual_source and not (root / visual_source).is_file():
            issues.append(f"{label} missing visual capture: {visual_source}")

    if seen_pairs != EXPECTED_PAIRS:
        issues.append("archive_clips must contain exactly the eight approved case/artifact pairs")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path, help="Path to source-audio-map.json")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument(
        "--require-captures", action="store_true", help="Require every browser visual source"
    )
    args = parser.parse_args()
    issues = verify_audio_map(args.map, args.root, args.require_captures)
    if issues:
        print("V3 source-audio map validation failed:", file=sys.stderr)
        print(*(f"- {issue}" for issue in issues), sep="\n", file=sys.stderr)
        return 2
    print("V3 source-audio map is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
