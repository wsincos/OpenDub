import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { MethodAtlasPage } from "./MethodAtlasPage";

describe("MethodAtlasPage", () => {
  it("presents the three complete dubbing methods as separate paths", () => {
    render(<MemoryRouter><MethodAtlasPage /></MemoryRouter>);

    expect(screen.getAllByRole("heading", { name: "HPMDubbing" })).toHaveLength(2);
    expect(screen.getByRole("heading", { name: "StyleDubber" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "EmoDubber" })).toBeVisible();
    expect(screen.getAllByRole("link", { name: /explore method/i })).toHaveLength(3);
    expect(screen.getByRole("link", { name: "Prepare an HPMDubbing project" })).toHaveAttribute("href", "/studio?method=hpmdubbing");
    expect(screen.getByRole("link", { name: "Prepare a StyleDubber project" })).toHaveAttribute("href", "/studio?method=styledubber");
    expect(screen.getByRole("link", { name: "Prepare an EmoDubber project" })).toHaveAttribute("href", "/studio?method=emodubber");
  });

  it("turns a declared primary need into an evidence-aware complete-method orientation", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><MethodAtlasPage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: /explicit emotion direction/i }));

    expect(screen.getByText(/recommended for inspection and preparation/i)).toBeVisible();
    expect(screen.getByText("EmoDubber", { selector: ".decision-result h2" })).toBeVisible();
    expect(screen.getByRole("link", { name: "Prepare an EmoDubber project from this recommendation" })).toHaveAttribute("href", "/studio?method=emodubber");
    expect(screen.getByText(/not a claim of live runtime or global superiority/i)).toBeVisible();
  });
});
