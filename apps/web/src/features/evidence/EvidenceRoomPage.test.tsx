import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, test } from "vitest";

import { EvidenceRoomPage } from "./EvidenceRoomPage";

test("renders a dark evidence observatory with source lines and an honest runtime boundary", () => {
  render(<MemoryRouter><EvidenceRoomPage /></MemoryRouter>);

  expect(screen.getByText("EVIDENCE OBSERVATORY")).toBeVisible();
  expect(screen.getByRole("heading", { name: "A source record is not yet a runnable method." })).toBeVisible();
  expect(screen.getByText("3 SOURCE RECORDS / 0 ADMITTED RUNTIMES")).toBeVisible();
  expect(screen.getByText("METHOD SOURCE LINES")).toBeVisible();
  expect(screen.getByText("RUNTIME ADMISSION RAIL")).toBeVisible();
  expect(screen.getAllByText("MIT")).toHaveLength(3);
  expect(screen.getAllByText("Weight terms not verified")).toHaveLength(3);
  expect(screen.getAllByText("Runtime unavailable")).toHaveLength(3);
  expect(screen.getAllByText("Concept only")).toHaveLength(3);
  expect(screen.getAllByText("TEAM-DEVELOPED COMPLETE METHOD")).toHaveLength(3);
  expect(screen.getAllByText("PUBLISHED RECORD")).toHaveLength(3);
  expect(screen.getByRole("link", { name: "Open HPMDubbing source at f50dfa7" })).toBeVisible();
  expect(screen.queryByText("Live ready")).not.toBeInTheDocument();
});
