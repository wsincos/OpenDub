import { describe, expect, it } from "vitest";

import { selectPeakWindow } from "./useAudioFeature";

describe("selectPeakWindow", () => {
  it("keeps the highest-energy contiguous window from a waveform feature", () => {
    expect(selectPeakWindow([0.02, 0.04, 0.81, 0.72, 0.64, 0.03], 3)).toEqual([0.81, 0.72, 0.64]);
  });

  it("returns a short feature unchanged", () => {
    expect(selectPeakWindow([0.2, 0.4], 3)).toEqual([0.2, 0.4]);
  });
});
