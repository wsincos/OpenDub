import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useSynchronizedArchivePlayback } from "./useSynchronizedArchivePlayback";

function makePlayer() {
  const player = document.createElement("video");
  Object.defineProperty(player, "pause", { configurable: true, value: vi.fn() });
  return player;
}

function makeTrackedPlayer() {
  const player = makePlayer();
  let value = 0;
  let writes = 0;
  Object.defineProperty(player, "currentTime", {
    configurable: true,
    get: () => value,
    set: (next: number) => {
      writes += 1;
      value = next;
    },
  });
  return { player, resetWrites: () => { writes = 0; }, writes: () => writes };
}

describe("useSynchronizedArchivePlayback", () => {
  it("switches to a matching archived source at the shared time without moving inactive video", () => {
    const { result } = renderHook(() => useSynchronizedArchivePlayback());
    const reference = makePlayer();
    const hpm = makePlayer();
    const style = makePlayer();

    act(() => {
      result.current.registerTrack("reference", reference);
      result.current.registerTrack("hpm", hpm);
      result.current.registerTrack("style", style);
      result.current.selectTrack("hpm");
      hpm.currentTime = 0.8;
      result.current.updateCurrentTime("hpm", 0.8);
      result.current.selectTrack("style");
    });

    expect(result.current.activeTrackId).toBe("style");
    expect(result.current.currentTime).toBe(0.8);
    expect(hpm.pause).toHaveBeenCalled();
    expect(hpm.currentTime).toBe(0.8);
    expect(style.currentTime).toBe(0.8);
    expect(hpm.muted).toBe(true);
    expect(style.muted).toBe(false);
    expect(reference.muted).toBe(true);
  });

  it("seeks every prepared source without requesting playback", () => {
    const { result } = renderHook(() => useSynchronizedArchivePlayback());
    const reference = makePlayer();
    const hpm = makePlayer();

    act(() => {
      result.current.registerTrack("reference", reference);
      result.current.registerTrack("hpm", hpm);
      result.current.seek(1.31);
    });

    expect(reference.currentTime).toBe(1.31);
    expect(hpm.currentTime).toBe(1.31);
    expect(reference.pause).not.toHaveBeenCalled();
    expect(hpm.pause).not.toHaveBeenCalled();
  });

  it("records an active video's time updates without seeking that same playing element", () => {
    const { result } = renderHook(() => useSynchronizedArchivePlayback());
    const tracked = makeTrackedPlayer();

    act(() => {
      result.current.registerTrack("reference", tracked.player);
      result.current.selectTrack("reference");
    });
    tracked.resetWrites();

    act(() => result.current.updateCurrentTime("reference", 0.74));

    expect(tracked.writes()).toBe(0);
    expect(result.current.currentTime).toBe(0.74);
  });

  it("resets every source to the first frame when the reader changes scene", () => {
    const { result } = renderHook(() => useSynchronizedArchivePlayback());
    const reference = makePlayer();
    const hpm = makePlayer();

    act(() => {
      result.current.registerTrack("reference", reference);
      result.current.registerTrack("hpm", hpm);
      result.current.seek(1.1);
      result.current.reset();
    });

    expect(reference.pause).toHaveBeenCalled();
    expect(hpm.pause).toHaveBeenCalled();
    expect(reference.currentTime).toBe(0);
    expect(hpm.currentTime).toBe(0);
    expect(result.current.activeTrackId).toBeNull();
    expect(result.current.currentTime).toBe(0);
  });
});
