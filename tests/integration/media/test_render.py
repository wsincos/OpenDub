from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from opendub.domain.time import TimeRange
from opendub.media.render import TimelineAudioClip, assemble_dubbing_track


def write_wav(path: Path, values: np.ndarray) -> None:
    sf.write(path, values, 24_000, subtype="PCM_16")


def test_assemble_track_places_audio_and_fills_silence(tmp_path: Path) -> None:
    first = tmp_path / "first.wav"
    second = tmp_path / "second.wav"
    output = tmp_path / "dubbing.wav"
    write_wav(first, np.full(12_000, 0.2, dtype=np.float32))
    write_wav(second, np.full(12_000, -0.2, dtype=np.float32))

    assemble_dubbing_track(
        (
            TimelineAudioClip("segment-1", TimeRange(0, 500_000), first),
            TimelineAudioClip("segment-2", TimeRange(1_000_000, 1_500_000), second),
        ),
        output,
        sample_rate=24_000,
    )
    rendered, sample_rate = sf.read(output, dtype="float32")

    assert sample_rate == 24_000
    assert len(rendered) == 36_000
    assert rendered[0] > 0.19
    assert abs(rendered[18_000]) < 1e-4
    assert rendered[24_000] < -0.19


def test_assemble_track_rejects_overlapping_segments(tmp_path: Path) -> None:
    source = tmp_path / "source.wav"
    write_wav(source, np.zeros(24_000, dtype=np.float32))

    with pytest.raises(ValueError, match="segment-1.*segment-2"):
        assemble_dubbing_track(
            (
                TimelineAudioClip("segment-1", TimeRange(0, 1_000_000), source),
                TimelineAudioClip("segment-2", TimeRange(500_000, 1_500_000), source),
            ),
            tmp_path / "out.wav",
            sample_rate=24_000,
        )
