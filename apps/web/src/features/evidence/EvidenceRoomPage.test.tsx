import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, test } from "vitest";

import { EvidenceRoomPage } from "./EvidenceRoomPage";

test("renders a provenance row and honest runtime boundary for every core method", () => {
  render(<MemoryRouter><EvidenceRoomPage /></MemoryRouter>);

  expect(screen.getByRole("heading", { name: "Evidence is part of the method." })).toBeVisible();
  expect(screen.getAllByText("MIT")).toHaveLength(3);
  expect(screen.getAllByText("Weight terms not verified")).toHaveLength(3);
  expect(screen.getAllByText("Runtime unavailable")).toHaveLength(3);
  expect(screen.getAllByText("Concept only")).toHaveLength(3);
  expect(screen.getByRole("link", { name: "Open HPMDubbing source at f50dfa7" })).toBeVisible();
  expect(screen.queryByText("Live ready")).not.toBeInTheDocument();
});
