import { useEffect, useState } from "react";

export type AudioFeature = {
  waveform_peaks: number[];
  times_seconds: number[];
  energy: number[];
  f0_hz: Array<number | null>;
};

export function useAudioFeature(path: string): AudioFeature | null {
  const [feature, setFeature] = useState<AudioFeature | null>(null);

  useEffect(() => {
    let active = true;
    if (import.meta.env.MODE === "test") return () => { active = false; };
    if (typeof fetch !== "function") return () => { active = false; };

    fetch(path)
      .then((response) => response.ok ? response.json() : null)
      .then((payload: AudioFeature | null) => { if (active) setFeature(payload); })
      .catch(() => { if (active) setFeature(null); });

    return () => { active = false; };
  }, [path]);

  return feature;
}

export function selectPeakWindow(peaks: number[], windowSize: number): number[] {
  if (peaks.length <= windowSize) return peaks;

  let bestStart = 0;
  let bestEnergy = -Infinity;
  for (let start = 0; start <= peaks.length - windowSize; start += 1) {
    const energy = peaks.slice(start, start + windowSize).reduce((sum, peak) => sum + peak, 0);
    if (energy > bestEnergy) {
      bestEnergy = energy;
      bestStart = start;
    }
  }

  return peaks.slice(bestStart, bestStart + windowSize);
}
