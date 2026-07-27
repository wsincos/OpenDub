import { useCallback, useEffect, useRef, useState } from "react";

export type ShowcasePlayback = {
  artifactPath: string;
  caseId: string;
  isPlaying: boolean;
};

function playerKey(caseId: string, artifactPath: string) {
  return `${caseId}:${artifactPath}`;
}

function resetPlayer(player: HTMLVideoElement) {
  player.pause();
  player.muted = true;

  try {
    player.currentTime = 0;
  } catch {
    // A not-yet-seekable browser media element is already stopped and muted.
  }
}

export function useExclusiveShowcasePlayback() {
  const players = useRef(new Map<string, HTMLVideoElement>());
  const [activePlayback, setActivePlayback] = useState<ShowcasePlayback | null>(null);

  const registerPlayer = useCallback((caseId: string, artifactPath: string, player: HTMLVideoElement | null) => {
    const key = playerKey(caseId, artifactPath);
    if (player) players.current.set(key, player);
    else players.current.delete(key);
  }, []);

  const resetAll = useCallback(() => {
    players.current.forEach(resetPlayer);
    setActivePlayback(null);
  }, []);

  const handlePlay = useCallback((caseId: string, artifactPath: string, current: HTMLVideoElement) => {
    const activeKey = playerKey(caseId, artifactPath);
    players.current.set(activeKey, current);
    players.current.forEach((player, key) => {
      if (key !== activeKey) resetPlayer(player);
    });
    current.muted = false;
    setActivePlayback({ artifactPath, caseId, isPlaying: true });
  }, []);

  const handlePause = useCallback((caseId: string, artifactPath: string) => {
    setActivePlayback((current) => (
      current?.caseId === caseId && current.artifactPath === artifactPath
        ? { ...current, isPlaying: false }
        : current
    ));
  }, []);

  useEffect(() => () => {
    players.current.forEach(resetPlayer);
  }, []);

  return { activePlayback, handlePause, handlePlay, registerPlayer, resetAll };
}
