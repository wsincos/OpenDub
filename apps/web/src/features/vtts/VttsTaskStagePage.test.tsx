import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { VttsTaskStagePage } from "./VttsTaskStagePage";

describe("VttsTaskStagePage", () => {
  it("makes the three VTTS inputs, complete method, and two outputs inspectable", () => {
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    expect(screen.getByRole("heading", { name: /video dubbing turns a scene into speech/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /silent video input/i })).toBeVisible();
    const filmstrip = screen.getByLabelText("Five-frame silent video filmstrip");
    expect(filmstrip).toHaveClass("filmstrip");
    expect(filmstrip.querySelectorAll(".filmstrip-frame")).toHaveLength(5);
    expect(screen.getByRole("button", { name: /text input/i })).toBeVisible();
    expect(screen.getByText("Reference + target text timing")).toBeVisible();
    expect(screen.getByRole("button", { name: /authorized reference speech input/i })).toBeVisible();
    expect(screen.getByRole("link", { name: /inspect complete methods/i })).toHaveAttribute("href", "/methods");
    expect(screen.getByText("TARGET SPEECH", { exact: true })).toBeVisible();
    expect(screen.getByLabelText("Reference contour")).toHaveAttribute("data-illustration", "reference-contour");
    expect(screen.getByLabelText("Target speech illustration")).toHaveAttribute("data-illustration", "target-speech");
    expect(screen.getByText("DUBBED VIDEO", { exact: true })).toBeVisible();
    const preview = screen.getByLabelText(/looping dubbed video preview/i);
    expect(preview).toHaveAttribute("autoplay");
    expect(preview).toHaveAttribute("loop");
    expect(preview).toHaveAttribute("muted");
    expect(preview).toHaveAttribute("src", "/showcases/v2/human-0/emodubber.mp4");
    expect(screen.getByRole("region", { name: "Task illustration" })).toHaveTextContent("One scene carries several timing cues.");
    expect(screen.queryByText("METHOD EXAMPLES")).not.toBeInTheDocument();
  });

  it("keeps the Task illustration separate from the synchronized timeline overview", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    await user.click(screen.getByRole("button", { name: /play task flow/i }));

    expect(screen.getByRole("button", { name: /pause task flow/i })).toBeVisible();
    const illustration = screen.getByRole("region", { name: "Task illustration" });
    const overview = screen.getByRole("region", { name: "Synchronized timeline overview" });
    expect(illustration).toHaveTextContent("One scene carries several timing cues.");
    expect(overview).toHaveTextContent("ONE SYNCHRONIZED TIMELINE");
    expect(within(illustration).queryByText("ONE SYNCHRONIZED TIMELINE")).not.toBeInTheDocument();
  });

  it("inspects video, text, and reference audio directly from the Task input cards", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    expect(screen.getByRole("region", { name: "Task illustration" })).toHaveTextContent("One scene carries several timing cues.");

    await user.click(screen.getByRole("button", { name: "Text input" }));

    expect(screen.getByRole("region", { name: "Task illustration" })).toHaveTextContent("Reference and target text share one timing view.");
    expect(screen.getByText("REFERENCE TEXT")).toBeVisible();
    expect(screen.getByText("TARGET TEXT")).toBeVisible();

    await user.click(screen.getByRole("button", { name: "Authorized reference speech input" }));

    expect(screen.getByRole("region", { name: "Task illustration" })).toHaveTextContent("Reference audio anchors identity and style.");
    expect(screen.getByLabelText("Reference identity waveform")).toHaveAttribute("data-illustration", "reference-identity");
  });

  it("keeps task illustrations independent from archived acoustic feature files", () => {
    const { container } = render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    expect(container.querySelectorAll("[data-feature-source]")).toHaveLength(0);
    expect(container.innerHTML).not.toContain("/showcases/v2/human-0/features/");
  });

  it("uses a compact overview layout when the task-flow capture explicitly requests it", () => {
    const originalUrl = window.location.href;
    window.history.replaceState({}, "", "/vtts?tour=flow&capture=overview");

    render(<MemoryRouter><VttsTaskStagePage /></MemoryRouter>);

    expect(screen.getByRole("region", { name: "Video text to speech task flow" })).toHaveClass("vtts-flow--capture-overview");
    window.history.replaceState({}, "", originalUrl);
  });
});
