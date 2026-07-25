import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { MethodAtlasPage } from "./MethodAtlasPage";

describe("MethodAtlasPage", () => {
  it("presents the three complete dubbing methods as separate paths", () => {
    render(<MemoryRouter><MethodAtlasPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "HPMDubbing" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "StyleDubber" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "EmoDubber" })).toBeVisible();
    expect(screen.getAllByRole("link", { name: /explore method/i })).toHaveLength(3);
  });
});
