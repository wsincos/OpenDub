import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useExclusiveShowcasePlayback } from "./useExclusiveShowcasePlayback";

function makePlayer() {
  const player = document.createElement("video");
  Object.defineProperty(player, "pause", { configurable: true, value: vi.fn() });
  return player;
}

describe("useExclusiveShowcasePlayback", () => {
  it("plays only the selected artifact and resets every other player", () => {
    const { result } = renderHook(() => useExclusiveShowcasePlayback());
    const gt = makePlayer();
    const hpm = makePlayer();
    const style = makePlayer();

    gt.currentTime = 1.2;
    hpm.currentTime = 1.1;

    act(() => {
      result.current.registerPlayer("human-0", "gt.mp4", gt);
      result.current.registerPlayer("human-0", "hpmdubbing.mp4", hpm);
      result.current.registerPlayer("human-0", "styledubber.mp4", style);
      result.current.handlePlay("human-0", "styledubber.mp4", style);
    });

    expect(result.current.activePlayback).toEqual({ caseId: "human-0", artifactPath: "styledubber.mp4", isPlaying: true });
    expect(gt.pause).toHaveBeenCalledOnce();
    expect(hpm.pause).toHaveBeenCalledOnce();
    expect(gt.currentTime).toBe(0);
    expect(hpm.currentTime).toBe(0);
    expect(gt.muted).toBe(true);
    expect(hpm.muted).toBe(true);
    expect(style.muted).toBe(false);
  });
});
