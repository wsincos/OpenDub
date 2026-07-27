import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { ExampleGalleryPage } from "./ExampleGalleryPage";

describe("ExampleGalleryPage", () => {
  it("shows the provided human and animated historical examples without claiming a fresh run", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><ExampleGalleryPage /></MemoryRouter>);

    expect(screen.getByRole("tab", { name: /human portrait/i })).toHaveAttribute("aria-selected", "true");
    expect(screen.getByText("Ground truth")).toBeVisible();
    expect(screen.getByText("HPMDubbing")).toBeVisible();
    expect(screen.getByText("StyleDubber")).toBeVisible();
    expect(screen.getByText("EmoDubber")).toBeVisible();
    expect(screen.getByText(/archived research example\. not a fresh opendub run/i)).toBeVisible();

    const gtPlayer = screen.getByLabelText(/human portrait case, ground truth/i) as HTMLVideoElement;
    const hpmPlayer = screen.getByLabelText(/human portrait case, hpmdubbing/i) as HTMLVideoElement;
    const stylePlayer = screen.getByLabelText(/human portrait case, styledubber/i) as HTMLVideoElement;
    const gtPause = vi.spyOn(gtPlayer, "pause").mockImplementation(() => undefined);
    const hpmPause = vi.spyOn(hpmPlayer, "pause").mockImplementation(() => undefined);

    fireEvent.play(stylePlayer);

    expect(gtPause).toHaveBeenCalled();
    expect(hpmPause).toHaveBeenCalled();
    expect(screen.getByText("AUDIBLE: StyleDubber")).toBeVisible();
    expect(screen.queryByText("AUDIBLE: Ground truth")).not.toBeInTheDocument();
    expect(stylePlayer.closest("article")).toHaveClass("is-active-artifact");

    await user.click(screen.getByRole("tab", { name: /animated character/i }));

    expect(stylePlayer.currentTime).toBe(0);
    expect(screen.getByRole("tab", { name: /animated character/i })).toHaveAttribute("aria-selected", "true");
    expect(screen.getByLabelText(/animated character case, ground truth/i)).toBeVisible();
  });
});
