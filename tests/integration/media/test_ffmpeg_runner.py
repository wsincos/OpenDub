from __future__ import annotations

import json
import subprocess
import wave
from pathlib import Path

from opendub.media.audio import normalize_reference_audio
from opendub.media.ffmpeg import FfmpegRunner
from opendub.media.probe import probe_media
from opendub.media.render import mux_video


def test_normalize_and_probe_synthetic_wav_with_ffmpeg(tmp_path: Path) -> None:
    source = tmp_path / "synthetic input.wav"
    destination = tmp_path / "normalized.wav"
    with wave.open(str(source), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(8_000)
        wav.writeframes(b"\x00\x00" * 16_000)

    normalize_reference_audio(source, destination, runner=FfmpegRunner())
    probe = probe_media(destination)

    assert destination.is_file()
    assert probe.audio_channels == 1
    assert probe.audio_sample_rate == 24_000
    assert probe.duration_us == 1_000_000


def test_muxed_video_has_ai_generated_dubbing_metadata(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    dubbing = tmp_path / "dubbing.wav"
    destination = tmp_path / "dubbed.mp4"
    subprocess.run(
        (
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=32x32:d=1",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=24000:cl=mono",
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(source),
        ),
        check=True,
        capture_output=True,
        text=True,
    )
    with wave.open(str(dubbing), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24_000)
        wav.writeframes(b"\x00\x00" * 24_000)

    mux_video(source, dubbing, destination, mode="remove")
    inspected = subprocess.run(
        (
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format_tags=comment",
            "-of",
            "json",
            str(destination),
        ),
        check=True,
        capture_output=True,
        text=True,
    )

    tags = json.loads(inspected.stdout)["format"]["tags"]
    assert tags["comment"] == "AI-generated dubbing by OpenDub"
