import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { OpenDubSummaryPage } from "./OpenDubSummaryPage";

describe("OpenDubSummaryPage", () => {
  it("summarizes team-developed complete methods and the platform workflow", () => {
    render(<MemoryRouter><OpenDubSummaryPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "OpenDub" })).toBeVisible();
    expect(screen.getByText("TEAM-DEVELOPED COMPLETE METHODS")).toBeVisible();
    expect(screen.getByText("HPMDubbing")).toBeVisible();
    expect(screen.getByText("StyleDubber")).toBeVisible();
    expect(screen.getByText("EmoDubber")).toBeVisible();
    expect(screen.getByText("InstructDubber")).toBeVisible();
    expect(screen.getByText("Speaker2Dub")).toBeVisible();
    expect(screen.getByRole("link", { name: /^Methods/ })).toHaveAttribute("href", "/methods");
    expect(screen.getByRole("link", { name: /^Examples/ })).toHaveAttribute("href", "/examples");
    expect(screen.getByRole("link", { name: /^Compare/ })).toHaveAttribute("href", "/compare");
    expect(screen.getByRole("link", { name: /^Evidence/ })).toHaveAttribute("href", "/evidence");
    expect(screen.getByRole("link", { name: /^Studio/ })).toHaveAttribute("href", "/studio");
    expect(screen.getAllByText("OPEN DEVELOPMENT").length).toBeGreaterThan(0);
  });
});
