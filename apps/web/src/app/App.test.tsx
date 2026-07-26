import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { OpenDubApp } from "./App";

describe("OpenDubApp", () => {
  it("opens the VTTS task stage at the root route", () => {
    render(<MemoryRouter initialEntries={["/"]}><OpenDubApp /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: /video dubbing turns a scene into speech/i })).toBeVisible();
    expect(screen.getByRole("link", { name: "Task" })).toHaveAttribute("aria-current", "page");
  });
});
