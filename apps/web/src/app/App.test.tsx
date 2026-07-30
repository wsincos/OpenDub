import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { OpenDubApp } from "./App";

describe("OpenDubApp", () => {
  it("consolidates the legacy Explore route into Task", () => {
    render(<MemoryRouter initialEntries={["/explore"]}><OpenDubApp /></MemoryRouter>);

    expect(screen.getByRole("link", { name: "Task" })).toBeVisible();
    expect(screen.queryByRole("link", { name: "Explore" })).not.toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /video dubbing turns a scene into speech/i })).toBeVisible();
  });
});
