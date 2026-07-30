import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { MethodAtlasPage } from "./MethodAtlasPage";

describe("MethodAtlasPage", () => {
  it("presents original complete methods and an evidence-limited expanding catalog", () => {
    render(<MemoryRouter><MethodAtlasPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "Multiple original methods. One shared dubbing task." })).toBeVisible();
    expect(screen.getByRole("button", { name: "Inspect HPMDubbing original method" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Inspect StyleDubber original method" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Inspect EmoDubber original method" })).toBeVisible();
    expect(screen.getAllByText("TEAM-DEVELOPED COMPLETE METHOD")).toHaveLength(3);
    expect(screen.getByText("PUBLISHED RECORD")).toBeVisible();
    expect(screen.getByLabelText("Expanding methods in OpenDub")).toHaveTextContent("InstructDubber");
    expect(screen.getByLabelText("Expanding methods in OpenDub")).toHaveTextContent("Speaker2Dub");
    expect(screen.getByText("In development in OpenDub.")).toBeVisible();
    expect(screen.getByRole("img", { name: "HPMDubbing original method architecture" })).toHaveAttribute("src", "/methods/papers/hpmdubbing-architecture.png");
    expect(screen.queryByText("CVPR · 2023")).not.toBeInTheDocument();
  });

  it("switches the original method reader without ranking the methods", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><MethodAtlasPage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: "Inspect EmoDubber original method" }));

    expect(screen.getByRole("img", { name: "EmoDubber original method architecture" })).toHaveAttribute("src", "/methods/papers/emodubber-architecture.png");
    expect(screen.getByText("Flow-based User Emotion Controlling")).toBeVisible();
    expect(screen.queryByText(/recommended for inspection/i)).not.toBeInTheDocument();
  });
});
