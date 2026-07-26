"""Deterministic, dependency-light audio features for showcase evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.floating[Any]]


@dataclass(frozen=True)
class AudioFeatures:
    """Compact feature arrays that can be traced back to one decoded audio asset."""

    duration_seconds: float
    waveform_peaks: tuple[float, ...]
    times_seconds: tuple[float, ...]
    energy: tuple[float, ...]
    f0_hz: tuple[float | None, ...]
    mel: tuple[tuple[float, ...], ...]


def analyze_pcm(
    samples: FloatArray,
    *,
    sample_rate: int,
    waveform_bins: int = 192,
    frame_size: int = 1024,
    hop_size: int = 256,
    mel_bands: int = 48,
) -> AudioFeatures:
    """Derive display features from mono PCM without inventing a speech signal."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if waveform_bins <= 0 or frame_size <= 0 or hop_size <= 0 or mel_bands <= 0:
        raise ValueError("analysis dimensions must be positive")

    mono: FloatArray = np.asarray(samples, dtype=np.float32).reshape(-1)
    duration_seconds = float(mono.size / sample_rate)
    waveform_peaks = _waveform_peaks(mono, waveform_bins)
    frames = _frames(mono, frame_size, hop_size)
    times = tuple(
        float((index * hop_size + frame_size / 2) / sample_rate) for index in range(len(frames))
    )
    rms: FloatArray = np.asarray(
        [np.sqrt(np.mean(frame * frame)) for frame in frames], dtype=np.float32
    )
    energy = _normalize(rms)
    f0 = tuple(_estimate_f0(frame, sample_rate) for frame in frames)
    mel = _log_mel(frames, sample_rate, mel_bands)

    return AudioFeatures(
        duration_seconds=duration_seconds,
        waveform_peaks=waveform_peaks,
        times_seconds=times,
        energy=energy,
        f0_hz=f0,
        mel=mel,
    )


def _waveform_peaks(samples: FloatArray, bins: int) -> tuple[float, ...]:
    if samples.size == 0:
        return tuple(0.0 for _ in range(bins))
    chunks = np.array_split(np.abs(samples), bins)
    return tuple(float(np.max(chunk)) if chunk.size else 0.0 for chunk in chunks)


def _frames(samples: FloatArray, frame_size: int, hop_size: int) -> tuple[FloatArray, ...]:
    if samples.size == 0:
        return (np.zeros(frame_size, dtype=np.float32),)
    frame_count = max(1, int(np.ceil((samples.size - frame_size) / hop_size)) + 1)
    padded_size = (frame_count - 1) * hop_size + frame_size
    padded: FloatArray = np.pad(samples, (0, max(0, padded_size - samples.size)))
    return tuple(
        padded[index * hop_size : index * hop_size + frame_size] for index in range(frame_count)
    )


def _normalize(values: FloatArray) -> tuple[float, ...]:
    maximum = float(np.max(values)) if values.size else 0.0
    if maximum <= 1e-8:
        return tuple(0.0 for _ in values)
    return tuple(float(value / maximum) for value in values)


def _estimate_f0(frame: FloatArray, sample_rate: int) -> float | None:
    centered = frame - np.mean(frame)
    signal_energy = float(np.dot(centered, centered))
    if signal_energy <= 1e-7:
        return None
    minimum_lag = max(1, int(sample_rate / 400))
    maximum_lag = min(len(centered) - 1, int(sample_rate / 70))
    if maximum_lag <= minimum_lag:
        return None
    autocorrelation = np.correlate(centered, centered, mode="full")[len(centered) - 1 :]
    normalized = autocorrelation / autocorrelation[0]
    search = normalized[minimum_lag : maximum_lag + 1]
    best_lag = int(np.argmax(search)) + minimum_lag
    if float(normalized[best_lag]) < 0.35:
        return None
    return float(sample_rate / best_lag)


def _log_mel(
    frames: tuple[FloatArray, ...], sample_rate: int, mel_bands: int
) -> tuple[tuple[float, ...], ...]:
    frame_size = len(frames[0])
    window: FloatArray = np.hanning(frame_size).astype(np.float32)
    spectrum: FloatArray = np.asarray(
        [np.abs(np.fft.rfft(frame * window)) ** 2 for frame in frames],
        dtype=np.float32,
    )
    filters = _mel_filterbank(sample_rate, frame_size, mel_bands)
    mel: FloatArray = np.log(np.maximum(spectrum @ filters.T, 1e-10))
    low = float(np.min(mel))
    high = float(np.max(mel))
    normalized = np.zeros_like(mel) if high - low <= 1e-8 else (mel - low) / (high - low)
    return tuple(tuple(float(value) for value in normalized[:, band]) for band in range(mel_bands))


def _mel_filterbank(sample_rate: int, frame_size: int, mel_bands: int) -> FloatArray:
    nyquist = sample_rate / 2
    minimum_mel = _hz_to_mel(0.0)
    maximum_mel = _hz_to_mel(nyquist)
    mel_points = np.linspace(minimum_mel, maximum_mel, mel_bands + 2)
    fft_bins = np.floor((frame_size + 1) * _mel_to_hz(mel_points) / sample_rate).astype(int)
    filters: FloatArray = np.zeros((mel_bands, frame_size // 2 + 1), dtype=np.float32)
    for band in range(mel_bands):
        left, center, right = (int(value) for value in fft_bins[band : band + 3])
        center = max(center, left + 1)
        right = max(right, center + 1)
        center = min(center, filters.shape[1] - 1)
        right = min(right, filters.shape[1])
        for index in range(left, center):
            filters[band, index] = (index - left) / max(1, center - left)
        for index in range(center, right):
            filters[band, index] = (right - index) / max(1, right - center)
    return filters


def _hz_to_mel(value: float) -> float:
    return float(2595 * np.log10(1 + value / 700))


def _mel_to_hz(value: FloatArray) -> FloatArray:
    return np.asarray(700 * (10 ** (value / 2595) - 1), dtype=np.float32)
