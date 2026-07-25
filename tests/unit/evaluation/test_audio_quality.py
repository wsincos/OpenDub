import numpy as np

from opendub.evaluation.audio_quality import clipping_ratio, integrated_lufs, silence_ratio


def test_audio_quality_metrics_do_not_mask_clipping_or_silence() -> None:
    samples = np.array([0.0, 0.0, 0.25, -0.25, 1.0, -1.0], dtype=np.float32)

    assert silence_ratio(samples).value == 2 / 6
    assert clipping_ratio(samples).value == 2 / 6


def test_loudness_is_explicitly_unavailable_without_a_valid_loudness_backend() -> None:
    result = integrated_lufs(np.zeros(48_000, dtype=np.float32), sample_rate=48_000)

    assert result.status == "unavailable"
    assert result.value is None
