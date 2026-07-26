import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

import { EmoGuidanceView } from "./EmoGuidanceView";
import { HpmHierarchyView } from "./HpmHierarchyView";
import { StyleScaleView } from "./StyleScaleView";

test("HPM hierarchy keeps the three visual scales visible while changing focus", async () => {
  const user = userEvent.setup();
  render(<HpmHierarchyView />);

  expect(screen.getByText("Lip -> duration")).toBeVisible();
  expect(screen.getByText("Face -> F0 + energy")).toBeVisible();
  expect(screen.getByText("Scene -> global emotion")).toBeVisible();

  await user.click(screen.getByRole("button", { name: /face affect/i }));
  expect(screen.getByText("Face affect -> F0 + energy")).toBeVisible();
});

test("StyleDubber switches between frame and phoneme explanation scales", async () => {
  const user = userEvent.setup();
  render(<StyleScaleView />);

  expect(screen.getByText("Frame groups")).toBeVisible();
  await user.click(screen.getByRole("button", { name: "Phoneme scale" }));
  expect(screen.getByText("Grouped phoneme intervals")).toBeVisible();
});

test("EmoDubber intensity changes a conceptual flow view without generating audio", async () => {
  const user = userEvent.setup();
  const { container } = render(<EmoGuidanceView />);

  expect(screen.getByText("CONCEPTUAL FLOW VIEW")).toBeVisible();
  expect(screen.getByText("62% guidance intensity")).toBeVisible();
  fireEvent.change(screen.getByRole("slider", { name: "Concept emotion intensity" }), { target: { value: "86" } });

  expect(screen.getByText("86% guidance intensity")).toBeVisible();
  expect(screen.getByText("No new audio generated in Concept mode.")).toBeVisible();
  expect(container.querySelector("audio")).toBeNull();
});
