"""FFprobe JSON parsing for media metadata; no human-readable parsing."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MediaProbe:
    """A normalized subset of FFprobe's machine-readable media metadata."""

    duration_us: int
    format_name: str
    video_width: int | None
    video_height: int | None
    audio_sample_rate: int | None
    audio_channels: int | None


def probe_media(path: Path, *, executable: str = "ffprobe") -> MediaProbe:
    """Inspect a media file through FFprobe's JSON output."""
    completed = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-4_000:] or "FFprobe failed without stderr output.")
    return parse_probe_output(completed.stdout)


def parse_probe_output(output: str) -> MediaProbe:
    """Parse FFprobe JSON and normalize duration into integer microseconds."""
    try:
        document = json.loads(output)
    except json.JSONDecodeError as error:
        raise ValueError("FFprobe output is not valid JSON") from error
    if not isinstance(document, dict):
        raise ValueError("FFprobe output must be a JSON object")

    format_data = _mapping(document.get("format"))
    duration_seconds = _number(format_data.get("duration"))
    if duration_seconds is None or duration_seconds < 0:
        raise ValueError("FFprobe output has no valid duration")

    video_stream = _first_stream(document.get("streams"), "video")
    audio_stream = _first_stream(document.get("streams"), "audio")
    return MediaProbe(
        duration_us=round(duration_seconds * 1_000_000),
        format_name=_string(format_data.get("format_name")) or "unknown",
        video_width=_integer(video_stream.get("width")),
        video_height=_integer(video_stream.get("height")),
        audio_sample_rate=_integer(audio_stream.get("sample_rate")),
        audio_channels=_integer(audio_stream.get("channels")),
    )


def _first_stream(streams: object, stream_type: str) -> dict[str, Any]:
    if not isinstance(streams, list):
        return {}
    for stream in streams:
        if isinstance(stream, dict) and stream.get("codec_type") == stream_type:
            return stream
    return {}


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _integer(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _string(value: object) -> str | None:
    return value if isinstance(value, str) else None
