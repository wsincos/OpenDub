/** Deterministic illustrative contours for the task explanation, not archive media features. */
function createIllustratedPeaks(seed: number, length: number): number[] {
  return Array.from({ length }, (_, index) => {
    const phrase = (index % 17) / 16;
    const syllable = Math.sin((index + seed) * 0.71) * 0.12;
    const envelope = Math.max(0.05, Math.sin((phrase + 0.08) * Math.PI));
    return Math.min(0.96, Math.max(0.035, envelope * (0.52 + syllable + ((index % 5) * 0.035))));
  });
}

export const ILLUSTRATED_REFERENCE_CONTOUR = createIllustratedPeaks(3, 72);
export const ILLUSTRATED_TARGET_SPEECH = createIllustratedPeaks(9, 96);
