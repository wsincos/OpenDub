from __future__ import annotations

import numpy as np

from opendub.showcase.features import analyze_pcm


def test_analyze_pcm_derives_normalized_waveform_mel_and_voiced_pitch() -> None:
    sample_rate = 16_000
    time = np.arange(sample_rate, dtype=np.float32) / sample_rate
    samples = 0.5 * np.sin(2 * np.pi * 220 * time)

    features = analyze_pcm(
        samples,
        sample_rate=sample_rate,
        waveform_bins=64,
        frame_size=512,
        hop_size=160,
        mel_bands=16,
    )

    assert len(features.waveform_peaks) == 64
    assert max(features.waveform_peaks) > 0.45
    assert len(features.mel) == 16
    assert all(len(row) == len(features.times_seconds) for row in features.mel)
    assert len(features.f0_hz) == len(features.times_seconds)
    voiced = [value for value in features.f0_hz if value is not None]
    assert voiced
    assert 210 <= float(np.median(np.asarray(voiced))) <= 230
    assert all(0.0 <= value <= 1.0 for value in features.energy)


def test_analyze_pcm_marks_silence_as_unvoiced_without_fake_pitch() -> None:
    features = analyze_pcm(
        np.zeros(1_600, dtype=np.float32),
        sample_rate=16_000,
        waveform_bins=16,
        frame_size=400,
        hop_size=160,
        mel_bands=8,
    )

    assert set(features.waveform_peaks) == {0.0}
    assert set(features.energy) == {0.0}
    assert set(features.f0_hz) == {None}
