import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { ComparisonLabPage } from "./ComparisonLabPage";

describe("ComparisonLabPage", () => {
  it("indexes four admitted archives and leads with file-derived acoustic evidence", () => {
    render(<MemoryRouter><ComparisonLabPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "One archive, several original method readings." })).toBeVisible();
    expect(screen.getByText("SCENE INDEX")).toBeVisible();
    expect(screen.getByRole("button", { name: /Select Case 01: Animated cinematic scene/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /Select Case 02: Presenter and display scene/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /Select Case 03: Animated character scene/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /Select Case 04: Human portrait scene/i })).toBeVisible();
    expect(screen.getByText("ARCHIVED SAME-SCENE LISTENING")).toBeVisible();
    expect(screen.getByText("No automatic ranking. This archive does not yet establish a verified common-input benchmark.")).toBeVisible();
    expect(screen.getByText("FILE-DERIVED ACOUSTIC VIEW")).toBeVisible();
    expect(screen.getByText("LOG-MEL / SELECTED ARCHIVE AUDIO")).toBeVisible();
    expect(screen.getByText("ARCHIVE FRAME CONTACTS")).toBeVisible();
    expect(screen.getByText("ANALYSIS SCALE")).toBeVisible();
    expect(screen.getByText("READ THE ORIGINAL METHODS")).toBeVisible();
    expect(screen.getByText("PUBLISHED RECORD")).toBeVisible();
    expect(screen.queryByText("N/A")).not.toBeInTheDocument();
    expect(screen.queryByText(/你终于来了/)).not.toBeInTheDocument();
  });

  it("resets on a scene change and keeps the selected source video and audio paired within that scene", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><ComparisonLabPage /></MemoryRouter>);

    const case04 = screen.getByRole("button", { name: /Select Case 02: Presenter and display scene/i });
    await user.click(case04);

    expect(case04).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByLabelText("Case 02, active source: Reference performance")).toBeVisible();
    await user.click(screen.getByRole("button", { name: "Select HPMDubbing source" }));
    const hpm = screen.getByLabelText(/Case 02, HPMDubbing source/i) as HTMLVideoElement;
    const style = screen.getByLabelText(/Case 02, StyleDubber source/i) as HTMLVideoElement;
    const hpmPause = vi.spyOn(hpm, "pause").mockImplementation(() => undefined);
    hpm.currentTime = 4.14;
    fireEvent.timeUpdate(hpm);

    await user.click(screen.getByRole("button", { name: "Select StyleDubber source" }));

    expect(hpmPause).toHaveBeenCalled();
    expect(style.currentTime).toBe(4.14);
    expect(style.muted).toBe(false);
    expect(screen.getByLabelText("Case 02, active source: StyleDubber")).toBeVisible();
    expect(screen.getByText("READY TO PLAY · StyleDubber")).toBeVisible();
  });

  it("starts a newly selected source from its first frame after the previous source has finished", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><ComparisonLabPage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: /Select Case 02: Presenter and display scene/i }));
    await user.click(screen.getByRole("button", { name: "Select HPMDubbing source" }));
    const hpm = screen.getByLabelText(/Case 02, HPMDubbing source/i) as HTMLVideoElement;
    hpm.currentTime = 7.8;
    fireEvent.timeUpdate(hpm);
    fireEvent.ended(hpm);

    await user.click(screen.getByRole("button", { name: "Select StyleDubber source" }));

    const style = screen.getByLabelText(/Case 02, StyleDubber source/i) as HTMLVideoElement;
    expect(style.currentTime).toBe(0);
  });
});
