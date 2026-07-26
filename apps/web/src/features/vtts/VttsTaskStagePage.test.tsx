import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { VttsTaskStagePage } from "./VttsTaskStagePage";

describe("VttsTaskStagePage", () => {
  it("makes the three VTTS inputs, complete method, and two outputs inspectable", () => {
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: /video dubbing turns a scene into speech/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /silent video input/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /target text input/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /authorized reference speech input/i })).toBeVisible();
    expect(screen.getByRole("link", { name: /inspect complete methods/i })).toHaveAttribute("href", "/methods");
    expect(screen.getByText(/target speech/i)).toBeVisible();
    expect(screen.getByText(/dubbed video/i)).toBeVisible();
    expect(screen.getByAltText("Actual log-mel feature from human-0 ground truth")).toBeVisible();
  });

  it("offers a controllable flow and exposes face, lip, and environment cues", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: /play task flow/i }));

    expect(screen.getByRole("button", { name: /pause task flow/i })).toBeVisible();
    expect(screen.getByRole("button", { name: "Face cue" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Lip cue" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Environment cue" })).toBeVisible();
    await user.click(screen.getByRole("button", { name: "Environment cue" }));
    expect(screen.getByRole("button", { name: "Environment cue" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getAllByText(/task illustration/i)).toHaveLength(2);
  });
});
