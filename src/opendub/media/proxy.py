"""Deterministic proxy media commands for responsive local editing."""

from __future__ import annotations

from pathlib import Path

from opendub.media.ffmpeg import CommandRunner, FfmpegRunner, ensure_parent


def create_proxy(source: Path, destination: Path, *, runner: CommandRunner | None = None) -> None:
    """Create a 720p-or-smaller H.264 proxy without modifying the source file."""
    ensure_parent(destination)
    (runner or FfmpegRunner()).run(
        (
            "-y",
            "-i",
            str(source),
            "-vf",
            "scale=-2:min(720\\,ih)",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            str(destination),
        )
    )


def extract_cover(source: Path, destination: Path, *, runner: CommandRunner | None = None) -> None:
    """Extract the first decodable video frame as a still image."""
    ensure_parent(destination)
    (runner or FfmpegRunner()).run(
        ("-y", "-i", str(source), "-frames:v", "1", "-q:v", "2", str(destination))
    )
