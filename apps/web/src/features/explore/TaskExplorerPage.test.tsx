import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { TaskExplorerPage } from "./TaskExplorerPage";

describe("TaskExplorerPage", () => {
  it("explains the three task inputs and distinct research/product outputs", () => {
    render(<MemoryRouter><TaskExplorerPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: /video dubbing/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /video input/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /text input/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /reference speech input/i })).toBeVisible();
    expect(screen.getByRole("tab", { name: /generated speech/i })).toBeVisible();
    expect(screen.getByRole("tab", { name: /dubbed video/i })).toBeVisible();
    expect(screen.getByRole("link", { name: /explore three complete methods/i })).toHaveAttribute("href", "/methods");
  });
});
