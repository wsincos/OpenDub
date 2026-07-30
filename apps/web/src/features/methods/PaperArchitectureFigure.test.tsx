import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { getMethod } from "../../content/methods";
import { PaperArchitectureFigure } from "./PaperArchitectureFigure";
import { getPaperFigure } from "./paper-figures";

describe("PaperArchitectureFigure", () => {
  it("keeps the original method figure intact while letting a reader inspect named regions", async () => {
    const user = userEvent.setup();
    const method = getMethod("hpmdubbing");
    if (!method) throw new Error("HPMDubbing fixture is unavailable");

    render(<PaperArchitectureFigure method={method} />);

    expect(screen.getByRole("img", { name: "HPMDubbing original method architecture" })).toHaveAttribute("src", "/methods/papers/hpmdubbing-architecture.png");
    expect(screen.getByText(/original method architecture, published with the source record/i)).toBeVisible();
    expect(screen.getByRole("heading", { name: "Duration Aligner" })).toBeVisible();

    await user.click(screen.getByRole("button", { name: "Inspect Atmosphere Booster in original method figure" }));

    expect(screen.getByRole("heading", { name: "Atmosphere Booster" })).toBeVisible();
    expect(screen.getByText(/scene features are fused through cross-attention/i)).toBeVisible();
  });

  it("uses the reviewed calibration values as immutable source-figure reading regions", () => {
    const hpmdubbing = getMethod("hpmdubbing");
    const styledubber = getMethod("styledubber");
    const emodubber = getMethod("emodubber");
    if (!hpmdubbing || !styledubber || !emodubber) throw new Error("method fixtures are unavailable");

    expect(getPaperFigure(hpmdubbing).regions.find((region) => region.id === "atmosphere")).toMatchObject({ x: 53, y: 43.3, width: 20.07, height: 34.36 });
    expect(getPaperFigure(styledubber).regions.find((region) => region.id === "adapter")).toMatchObject({ x: 6.46, y: 26.91, width: 72.82, height: 38.66 });
    expect(getPaperFigure(styledubber).regions.find((region) => region.id === "decoder")).toMatchObject({ x: 35.71, y: 66.2, width: 31.43, height: 28.34 });
    expect(getPaperFigure(emodubber).regions.find((region) => region.id === "identity")).toMatchObject({ x: 2.8, y: 3, width: 56.77, height: 19.06 });
    expect(getPaperFigure(emodubber).regions.find((region) => region.id === "prosody")).toMatchObject({ x: 2.98, y: 26.2, width: 31.37, height: 44.07 });
    expect(getPaperFigure(emodubber).regions.find((region) => region.id === "pronunciation")).toMatchObject({ x: 35.59, y: 26.2, width: 22.59, height: 44.56 });
  });
});
