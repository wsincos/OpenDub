import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { TaskIllustrationPanel } from "./TaskIllustrationPanel";

describe("TaskIllustrationPanel", () => {
  it("uses the quiet task-illustration treatment for the selected input", () => {
    render(<TaskIllustrationPanel />);

    expect(screen.getByText(/one scene carries several timing cues/i)).toBeVisible();
    expect(screen.queryByText("ONE SYNCHRONIZED TIMELINE")).not.toBeInTheDocument();
  });

  it("provides matching illustration modules for text and reference audio", () => {
    const { rerender } = render(<TaskIllustrationPanel activeInput="text" />);

    expect(screen.getByText("Reference and target text share one timing view.")).toBeVisible();

    rerender(<TaskIllustrationPanel activeInput="reference" />);

    expect(screen.getByText("Reference audio anchors identity and style.")).toBeVisible();
    expect(screen.getByLabelText("Reference identity waveform")).toHaveAttribute("data-illustration", "reference-identity");
    expect(screen.getByText("ILLUSTRATED / NO ARCHIVE AUDIO OR TRANSCRIPT")).toBeVisible();
  });

  it("restores environment as an independently inspectable scene cue", async () => {
    const user = userEvent.setup();
    const { container } = render(<TaskIllustrationPanel />);

    expect(screen.getByRole("button", { name: /hide environment overlay/i })).toBeVisible();
    expect(container.querySelector(".task-illustration-environment")).toBeVisible();

    await user.click(screen.getByRole("button", { name: /hide environment overlay/i }));

    expect(container.querySelector(".task-illustration-environment")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /show environment overlay/i })).toBeVisible();
  });
});
