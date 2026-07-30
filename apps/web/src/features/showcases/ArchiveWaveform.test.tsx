import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ArchiveWaveform } from "./ArchiveWaveform";

vi.mock("../vtts/useAudioFeature", () => ({
  useAudioFeature: () => ({
    waveform_peaks: Array.from({ length: 120 }, (_, index) => index === 119 ? 1 : index / 240),
  }),
}));

describe("ArchiveWaveform", () => {
  it("renders the full PCM-derived peak envelope rather than an energy-selected excerpt", () => {
    render(<ArchiveWaveform color="#83d6c0" featureUrl="/fixture.json" label="Fixture" />);

    const waveform = screen.getByRole("img", { name: "Fixture waveform" });
    const lines = waveform.querySelectorAll("line");
    expect(lines).toHaveLength(120);
    expect(lines.item(0)).toHaveAttribute("y1", "15");
    expect(lines.item(119)).toHaveAttribute("y1", "2");
  });

  it("declares a bounded drawing surface so a waveform cannot use the SVG default viewport", () => {
    render(<ArchiveWaveform color="#83d6c0" featureUrl="/fixture.json" label="Fixture" />);

    const waveform = screen.getByRole("img", { name: "Fixture waveform" });
    expect(waveform).toHaveAttribute("width", "100%");
    expect(waveform).toHaveAttribute("height", "37");
  });
});
