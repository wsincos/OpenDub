import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { SynchronizedTimelinePanel } from "./SynchronizedTimelinePanel";

describe("SynchronizedTimelinePanel", () => {
  afterEach(() => vi.useRealTimers());

  it("starts at zero, runs for one seven-second pass, and pulses when playback begins", () => {
    vi.useFakeTimers();
    const { container } = render(<SynchronizedTimelinePanel />);

    expect(screen.getByText("00:00.0")).toBeVisible();
    expect(container.querySelector("[data-feature-source]")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Play illustrated timeline" }));

    expect(container.querySelector(".synchronized-timeline-play-pulse")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Pause illustrated timeline" })).toBeVisible();

    act(() => vi.advanceTimersByTime(7_000));

    expect(screen.getByText("00:07.0")).toBeVisible();
    expect(screen.getByRole("button", { name: "Play illustrated timeline" })).toBeVisible();

    act(() => vi.advanceTimersByTime(500));

    expect(screen.getByText("00:07.0")).toBeVisible();
  });
});
