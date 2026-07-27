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
    expect(screen.getByText("TARGET SPEECH", { exact: true })).toBeVisible();
    expect(screen.getByText("DUBBED VIDEO", { exact: true })).toBeVisible();
    expect(screen.getByText(/task illustration · concept scene/i)).toBeVisible();
  });

  it("offers a controllable flow and keeps the task illustration separate from archived examples", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: /play task flow/i }));

    expect(screen.getByRole("button", { name: /pause task flow/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /hide face overlay/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /hide lip overlay/i })).toBeVisible();
    await user.click(screen.getByRole("button", { name: /hide lip overlay/i }));
    expect(screen.queryByText("Lip motion", { exact: true })).not.toBeInTheDocument();
    expect(screen.getByText(/task illustration · no case audio or transcript/i)).toBeVisible();
  });
});
