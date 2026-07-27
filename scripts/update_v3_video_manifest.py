#!/usr/bin/env python3
"""Refresh hashes and stream facts for the V3 narrated evidence film."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def _read_object(path: Path) -> dict[str, Any]:
    value: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _probe(path: Path) -> dict[str, Any]:
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


def _read_json(value: str, label: str) -> dict[str, Any]:
    parsed: Any = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must be a JSON object")
    return parsed


def _find_stream(streams: list[Any], codec_type: str) -> dict[str, Any]:
    for stream in streams:
        if isinstance(stream, dict) and stream.get("codec_type") == codec_type:
            return stream
    raise ValueError(f"V3 delivery is missing a {codec_type} stream")


def _fps(value: str) -> int | float:
    numerator, denominator = (int(part) for part in value.split("/", maxsplit=1))
    rate = numerator / denominator
    return int(rate) if rate.is_integer() else rate


def _repository_revision(root: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def update_manifest(video_dir: Path) -> None:
    manifest_path = video_dir / "delivery-manifest.json"
    manifest = _read_object(manifest_path)
    video = manifest.get("video")
    if not isinstance(video, dict) or not isinstance(video.get("path"), str):
        raise ValueError("delivery manifest video.path must be a string")
    video_path = video_dir / video["path"]
    probe = _probe(video_path)
    streams = probe.get("streams")
    if not isinstance(streams, list):
        raise ValueError("ffprobe must return streams")
    video_stream = _find_stream(streams, "video")
    audio_stream = _find_stream(streams, "audio")
    subtitle_stream = _find_stream(streams, "subtitle")
    format_record = probe.get("format")
    if not isinstance(format_record, dict) or not isinstance(format_record.get("duration"), str):
        raise ValueError("ffprobe must return format duration")
    video.update(
        {
            "sha256": _sha256(video_path),
            "duration_seconds": round(float(format_record["duration"]), 3),
            "width": int(video_stream["width"]),
            "height": int(video_stream["height"]),
            "fps": _fps(str(video_stream["r_frame_rate"])),
            "audio": (
                f"{audio_stream['codec_name'].upper()}, {audio_stream['sample_rate']} Hz, "
                f"{'stereo' if int(audio_stream['channels']) == 2 else 'mono'}"
            ),
            "subtitle": f"{subtitle_stream['codec_name']}, Chinese and English",
        }
    )
    supporting = manifest.get("supporting_files")
    if not isinstance(supporting, list):
        raise ValueError("delivery manifest supporting_files must be a list")
    for item in supporting:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("each supporting file must have a path")
        item["sha256"] = _sha256(video_dir / item["path"])
    manifest["repository_baseline"] = _repository_revision(video_dir.parents[3])
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-dir", required=True, type=Path)
    args = parser.parse_args()
    update_manifest(args.video_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
