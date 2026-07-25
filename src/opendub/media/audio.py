"""Reference-audio normalization and lightweight deterministic checks."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]

from opendub.media.ffmpeg import CommandRunner, FfmpegRunner, ensure_parent


def normalize_reference_audio(
    source: Path,
    destination: Path,
    *,
    runner: CommandRunner | None = None,
) -> None:
    """Convert a reference to mono, 24 kHz PCM WAV through FFmpeg."""
    ensure_parent(destination)
    command_runner = runner or FfmpegRunner()
    command_runner.run(
        (
            "-y",
            "-i",
            str(source),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        )
    )


def analyze_audio(path: Path) -> tuple[float, float, int]:
    """Return silence ratio, clipping ratio, and duration samples for a WAV-like file."""
    samples, _sample_rate = sf.read(path, always_2d=True)
    values = np.asarray(samples, dtype=np.float32)
    if values.size == 0:
        return 1.0, 0.0, 0
    peak_by_frame = np.max(np.abs(values), axis=1)
    silence_ratio = float(np.mean(peak_by_frame < 1e-4))
    clipping_ratio = float(np.mean(peak_by_frame >= 0.999))
    return silence_ratio, clipping_ratio, int(values.shape[0])
