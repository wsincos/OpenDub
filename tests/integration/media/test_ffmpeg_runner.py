from __future__ import annotations

import wave
from pathlib import Path

from opendub.media.audio import normalize_reference_audio
from opendub.media.ffmpeg import FfmpegRunner
from opendub.media.probe import probe_media


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
