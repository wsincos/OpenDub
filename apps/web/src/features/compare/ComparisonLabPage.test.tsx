import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, test } from "vitest";

import { ComparisonLabPage } from "./ComparisonLabPage";

test("renders the evidence gate before any method ranking", () => {
  render(<MemoryRouter><ComparisonLabPage /></MemoryRouter>);

  expect(screen.getByRole("heading", { name: "Comparisons need the same scene." })).toBeInTheDocument();
  expect(screen.getByText("COMMON INPUT CASE")).toBeInTheDocument();
  expect(screen.getByText("Video fingerprint")).toBeInTheDocument();
  expect(screen.getByText("HPMDubbing")).toBeInTheDocument();
  expect(screen.getByText("StyleDubber")).toBeInTheDocument();
  expect(screen.getByText("EmoDubber")).toBeInTheDocument();
  expect(screen.getAllByText("No public replay bundle")).toHaveLength(3);
});
