import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { OpenDubCoverPage } from "./OpenDubCoverPage";

describe("OpenDubCoverPage", () => {
  it("presents an English-only editorial identity cover", () => {
    render(<MemoryRouter><OpenDubCoverPage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: "OpenDub" })).toBeVisible();
    expect(screen.getByText("OPEN-SOURCE RESEARCH PLATFORM")).toBeVisible();
    expect(screen.getByText("MULTIMODAL INTELLIGENT VIDEO DUBBING")).toBeVisible();
    expect(screen.getByText("MAKE VIDEO DUBBING INTELLIGIBLE.")).toBeVisible();
    expect(screen.getByLabelText("OpenDub input signal convergence")).toHaveTextContent("VIDEO");
    expect(screen.getByLabelText("OpenDub input signal convergence")).toHaveTextContent("TEXT");
    expect(screen.getByLabelText("OpenDub input signal convergence")).toHaveTextContent("REFERENCE SPEECH");
    expect(screen.getByLabelText("OpenDub input signal convergence")).toHaveTextContent("DUBBED VIDEO");
    expect(screen.queryByText("多模态智能视频配音开源平台")).not.toBeInTheDocument();
  });
});
