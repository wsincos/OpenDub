import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { MethodCanvasPage } from "./MethodCanvasPage";

describe("MethodCanvasPage", () => {
  it("selects a complete-method component and exposes its evidence-bound signals", async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={["/methods/hpmdubbing"]}>
        <Routes><Route element={<MethodCanvasPage />} path="/methods/:methodSlug" /></Routes>
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { name: "HPMDubbing" })).toBeVisible();
    await user.click(screen.getByRole("button", { name: "Inspect Face Affect" }));
    expect(screen.getByRole("heading", { name: "Face Affect" })).toBeVisible();
    expect(screen.getByText("Face ROI")).toBeVisible();
    expect(screen.getByText("F0")).toBeVisible();
  });

  it("removes a pinned signal from the shared dock", async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={["/methods/hpmdubbing"]}>
        <Routes><Route element={<MethodCanvasPage />} path="/methods/:methodSlug" /></Routes>
      </MemoryRouter>,
    );

    await user.click(screen.getByRole("button", { name: "Inspect Face Affect" }));
    await user.click(screen.getByRole("button", { name: "Face ROI" }));
    expect(screen.getByRole("button", { name: "Remove Face ROI" })).toBeVisible();

    await user.click(screen.getByRole("button", { name: "Remove Face ROI" }));
    expect(screen.queryByRole("button", { name: "Remove Face ROI" })).not.toBeInTheDocument();
  });

  it("renders the method-specific Concept panel for EmoDubber", () => {
    render(
      <MemoryRouter initialEntries={["/methods/emodubber"]}>
        <Routes><Route element={<MethodCanvasPage />} path="/methods/:methodSlug" /></Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("CONCEPTUAL FLOW VIEW")).toBeVisible();
    expect(screen.getByRole("slider", { name: "Concept emotion intensity" })).toBeVisible();
  });

  it("keeps a complete method's side inputs and semantic branches inspectable", async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={["/methods/hpmdubbing"]}>
        <Routes><Route element={<MethodCanvasPage />} path="/methods/:methodSlug" /></Routes>
      </MemoryRouter>,
    );

    expect(screen.getByRole("button", { name: "Inspect Reference speech" })).toBeVisible();
    expect(document.querySelector('[data-edge-id="reference-prosody"]')).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Inspect Reference speech" }));
    expect(screen.getByRole("heading", { name: "Reference speech" })).toBeVisible();
    expect(screen.getByText("Reference speech provides speaker information.")).toBeVisible();
  });
});
