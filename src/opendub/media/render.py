"""Deterministic audio assembly and shell-free final video muxing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]

from opendub.domain.time import TimeRange
from opendub.media.ffmpeg import CommandRunner, FfmpegRunner, ensure_parent

MixMode = Literal["preserve", "duck", "remove"]
AI_DUBBING_METADATA = "comment=AI-generated dubbing by OpenDub"


@dataclass(frozen=True)
class TimelineAudioClip:
    """A generated candidate assigned to exactly one non-overlapping target window."""

    segment_id: str
    range: TimeRange
    path: Path


def assemble_dubbing_track(
    clips: tuple[TimelineAudioClip, ...],
    destination: Path,
    *,
    sample_rate: int,
) -> None:
    """Place clips into a silent master WAV, cropping or padding to each time window."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    _validate_non_overlapping(clips)
    frame_count = max((_us_to_samples(clip.range.end_us, sample_rate) for clip in clips), default=0)
    master = np.zeros(frame_count, dtype=np.float32)
    for clip in clips:
        start = _us_to_samples(clip.range.start_us, sample_rate)
        end = _us_to_samples(clip.range.end_us, sample_rate)
        source, source_rate = sf.read(clip.path, dtype="float32", always_2d=True)
        if source_rate != sample_rate:
            raise ValueError(
                f"{clip.segment_id}: sample rate {source_rate} does not match {sample_rate}"
            )
        mono = np.mean(np.asarray(source, dtype=np.float32), axis=1)
        target_length = end - start
        master[start:end] = mono[:target_length]
    ensure_parent(destination)
    sf.write(destination, master, sample_rate, subtype="PCM_16")


def mux_video(
    video: Path,
    dubbing_audio: Path,
    destination: Path,
    *,
    mode: MixMode,
    runner: CommandRunner | None = None,
) -> None:
    """Mux the dubbing track with a video using an explicit original-audio policy."""
    ensure_parent(destination)
    command_runner = runner or FfmpegRunner()
    if mode == "remove":
        command_runner.run(
            (
                "-y",
                "-i",
                str(video),
                "-i",
                str(dubbing_audio),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-metadata",
                AI_DUBBING_METADATA,
                str(destination),
            )
        )
        return

    original_volume = "1.0" if mode == "preserve" else "0.2"
    command_runner.run(
        (
            "-y",
            "-i",
            str(video),
            "-i",
            str(dubbing_audio),
            "-filter_complex",
            f"[0:a]volume={original_volume}[original];[original][1:a]amix=inputs=2:normalize=0[mixed]",
            "-map",
            "0:v:0",
            "-map",
            "[mixed]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-metadata",
            AI_DUBBING_METADATA,
            str(destination),
        )
    )


def _validate_non_overlapping(clips: tuple[TimelineAudioClip, ...]) -> None:
    ordered = sorted(
        clips,
        key=lambda clip: (clip.range.start_us, clip.range.end_us, clip.segment_id),
    )
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current.range.start_us < previous.range.end_us:
            raise ValueError(f"overlapping segments: {previous.segment_id}, {current.segment_id}")


def _us_to_samples(time_us: int, sample_rate: int) -> int:
    return round(time_us * sample_rate / 1_000_000)
