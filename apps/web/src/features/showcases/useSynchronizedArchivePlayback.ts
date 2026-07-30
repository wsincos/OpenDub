import { useCallback, useEffect, useRef, useState } from "react";

export type ArchivePlaybackStatus = "idle" | "ready" | "playing" | "ended" | "error";

function setTime(player: HTMLVideoElement, time: number) {
  try {
    player.currentTime = time;
  } catch {
    // Browser media elements can reject a seek before metadata is available.
  }
}

export function useSynchronizedArchivePlayback() {
  const tracks = useRef(new Map<string, HTMLVideoElement>());
  const activeTrackRef = useRef<string | null>(null);
  const currentTimeRef = useRef(0);
  const [activeTrackId, setActiveTrackId] = useState<string | null>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [status, setStatus] = useState<ArchivePlaybackStatus>("idle");

  const registerTrack = useCallback((trackId: string, player: HTMLVideoElement | null) => {
    if (player) {
      player.muted = trackId !== activeTrackRef.current;
      tracks.current.set(trackId, player);
    } else {
      tracks.current.delete(trackId);
    }
  }, []);

  const selectTrack = useCallback((trackId: string) => {
    const sharedTime = currentTimeRef.current;
    tracks.current.forEach((player, id) => {
      if (id === trackId) {
        setTime(player, sharedTime);
        player.muted = false;
      } else {
        player.pause();
        player.muted = true;
      }
    });
    activeTrackRef.current = trackId;
    setActiveTrackId(trackId);
    setStatus("ready");
  }, []);

  const playActive = useCallback(async () => {
    const activeTrack = activeTrackRef.current;
    const player = activeTrack ? tracks.current.get(activeTrack) : undefined;
    if (!player) return;

    try {
      await player.play();
      setStatus("playing");
    } catch {
      setStatus("error");
    }
  }, []);

  const pauseActive = useCallback(() => {
    const activeTrack = activeTrackRef.current;
    const player = activeTrack ? tracks.current.get(activeTrack) : undefined;
    player?.pause();
    if (player) setStatus("ready");
  }, []);

  const seek = useCallback((time: number) => {
    currentTimeRef.current = time;
    tracks.current.forEach((player) => setTime(player, time));
    setCurrentTime(time);
  }, []);

  const reset = useCallback(() => {
    tracks.current.forEach((player) => {
      player.pause();
      player.muted = true;
      setTime(player, 0);
    });
    activeTrackRef.current = null;
    currentTimeRef.current = 0;
    setActiveTrackId(null);
    setCurrentTime(0);
    setStatus("idle");
  }, []);

  const updateCurrentTime = useCallback((trackId: string, time: number) => {
    if (activeTrackRef.current !== trackId) return;
    currentTimeRef.current = time;
    setCurrentTime(time);
  }, []);

  const handleEnded = useCallback((trackId: string) => {
    if (activeTrackRef.current === trackId) setStatus("ended");
  }, []);

  useEffect(() => () => {
    tracks.current.forEach((player) => {
      player.pause();
      player.muted = true;
    });
  }, []);

  return {
    activeTrackId,
    currentTime,
    handleEnded,
    pauseActive,
    playActive,
    registerTrack,
    reset,
    seek,
    selectTrack,
    status,
    updateCurrentTime,
  };
}
