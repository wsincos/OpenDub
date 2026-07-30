import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { ExampleGalleryPage } from "./ExampleGalleryPage";

describe("ExampleGalleryPage", () => {
  it("restores the compact two-family four-up archive gallery", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><ExampleGalleryPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "Inspect the work, not a promise." })).toBeVisible();
    expect(screen.getByRole("tab", { name: /human portrait/i })).toBeVisible();
    expect(screen.getByRole("tab", { name: /animated character/i })).toBeVisible();
    expect(screen.getAllByLabelText(/human portrait case,/i)).toHaveLength(4);
    expect(screen.getByText("REFERENCE PERFORMANCE")).toBeVisible();
    expect(screen.getAllByText("TEAM-DEVELOPED METHOD OUTPUT")).toHaveLength(3);
    expect(screen.getByText("Archived research example. Not a fresh OpenDub run.")).toBeVisible();
    expect(screen.queryByText(/CVPR 2023/i)).not.toBeInTheDocument();

    await user.click(screen.getByRole("tab", { name: /animated character/i }));

    expect(screen.getByRole("tab", { name: /animated character/i })).toHaveAttribute("aria-selected", "true");
    expect(screen.getAllByLabelText(/animated character case,/i)).toHaveLength(4);
    expect(screen.queryByRole("tab", { name: /cinematic/i })).not.toBeInTheDocument();
  });

  it("keeps four visible panels but permits only the panel that starts playback to be audible", () => {
    render(<MemoryRouter><ExampleGalleryPage /></MemoryRouter>);

    const hpm = screen.getByLabelText(/human portrait case, HPMDubbing/i) as HTMLVideoElement;
    const style = screen.getByLabelText(/human portrait case, StyleDubber/i) as HTMLVideoElement;
    const hpmPause = vi.spyOn(hpm, "pause").mockImplementation(() => undefined);
    fireEvent.play(style);

    expect(hpmPause).toHaveBeenCalled();
    expect(style.muted).toBe(false);
    expect(hpm.muted).toBe(true);
    expect(screen.getByText("AUDIBLE: StyleDubber")).toBeVisible();
  });
});
