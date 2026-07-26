#!/usr/bin/env python3
"""Refresh V2 video delivery hashes and stream facts after a deterministic rebuild."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-dir", required=True, type=Path)
    args = parser.parse_args()
    update_manifest(args.video_dir.resolve())
    return 0


def update_manifest(video_dir: Path) -> None:
    """Update the versioned manifest from the exported MP4 and supporting files."""
    manifest_path = video_dir / "delivery-manifest.json"
    manifest = _read_object(manifest_path)
    video_path = video_dir / _required_string(_required_object(manifest, "video"), "path")
    probe = _ffprobe(video_path)
    streams = probe.get("streams")
    if not isinstance(streams, list):
        raise ValueError("ffprobe must return a streams list")
    video_stream = _find_stream(streams, "video")
    audio_stream = _find_stream(streams, "audio")
    subtitle_stream = _find_stream(streams, "subtitle")
    video = _required_object(manifest, "video")
    video.update(
        {
            "sha256": _sha256(video_path),
            "duration_seconds": round(float(_required_object(probe, "format")["duration"]), 3),
            "width": _required_int(video_stream, "width"),
            "height": _required_int(video_stream, "height"),
            "fps": _fps(_required_string(video_stream, "r_frame_rate")),
            "audio": (
                f"{_required_string(audio_stream, 'codec_name').upper()}, "
                f"{_required_string(audio_stream, 'sample_rate')} Hz, "
                f"{'stereo' if _required_int(audio_stream, 'channels') == 2 else 'mono'}"
            ),
            "subtitle": _required_string(subtitle_stream, "codec_name") + ", Chinese and English",
        }
    )
    supporting = manifest.get("supporting_files")
    if not isinstance(supporting, list):
        raise ValueError("supporting_files must be a list")
    for item in supporting:
        if not isinstance(item, dict):
            raise ValueError("supporting file entry must be an object")
        item["sha256"] = _sha256(video_dir / _required_string(item, "path"))
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _ffprobe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return _read_json(result.stdout, "ffprobe output")


def _find_stream(streams: list[object], codec_type: str) -> dict[str, Any]:
    for stream in streams:
        if isinstance(stream, dict) and stream.get("codec_type") == codec_type:
            return stream
    raise ValueError(f"video delivery is missing a {codec_type} stream")


def _fps(value: str) -> int | float:
    numerator, denominator = (int(part) for part in value.split("/", maxsplit=1))
    rate = numerator / denominator
    return int(rate) if rate.is_integer() else rate


def _read_object(path: Path) -> dict[str, Any]:
    return _read_json(path.read_text(encoding="utf-8"), str(path))


def _read_json(value: str, label: str) -> dict[str, Any]:
    parsed: Any = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must be a JSON object")
    return parsed


def _required_object(value: dict[str, Any], key: str) -> dict[str, Any]:
    nested = value.get(key)
    if not isinstance(nested, dict):
        raise ValueError(f"{key} must be an object")
    return nested


def _required_string(value: dict[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item:
        raise ValueError(f"{key} must be a non-empty string")
    return item


def _required_int(value: dict[str, Any], key: str) -> int:
    item = value.get(key)
    if not isinstance(item, int):
        raise ValueError(f"{key} must be an integer")
    return item


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
