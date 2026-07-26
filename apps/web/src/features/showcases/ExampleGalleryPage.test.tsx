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

    const hpmPlayer = screen.getByLabelText(/human portrait case, hpmdubbing/i) as HTMLVideoElement;
    const pause = vi.spyOn(hpmPlayer, "pause");
    fireEvent.play(screen.getByLabelText(/human portrait case, ground truth/i));
    expect(pause).toHaveBeenCalled();

    await user.click(screen.getByRole("tab", { name: /animated character/i }));

    expect(screen.getByRole("tab", { name: /animated character/i })).toHaveAttribute("aria-selected", "true");
    expect(screen.getByLabelText(/animated character case, ground truth/i)).toBeVisible();
  });
});
