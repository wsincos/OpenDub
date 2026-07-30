import { CirclePause, CirclePlay, Layers3 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { TASK_ILLUSTRATION_IPA, TASK_ILLUSTRATION_SUBTITLE_TOKENS } from "./TaskIllustrationPanel";
import { ILLUSTRATED_TARGET_SPEECH } from "./illustrated-task-signals";
import "./synchronized-timeline-panel.css";

const TIMELINE_DURATION_SECONDS = 7;
const TIMELINE_TICK_MILLISECONDS = 70;
const FILMSTRIP_FRAME_COUNT = 24;

export function SynchronizedTimelinePanel() {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [pulseId, setPulseId] = useState(0);

  useEffect(() => {
    if (!playing) return undefined;
    const interval = window.setInterval(() => {
      setProgress((current) => {
        const next = Math.min(100, current + 1);
        if (next === 100) {
          window.clearInterval(interval);
          setPlaying(false);
        }
        return next;
      });
    }, TIMELINE_TICK_MILLISECONDS);
    return () => window.clearInterval(interval);
  }, [playing]);

  const timecode = useMemo(() => {
    const seconds = (progress / 100) * TIMELINE_DURATION_SECONDS;
    return `00:0${Math.floor(seconds)}.${Math.floor((seconds % 1) * 10)}`;
  }, [progress]);

  function togglePlayback() {
    setPulseId((current) => current + 1);
    if (playing) {
      setPlaying(false);
      return;
    }
    if (progress >= 100) setProgress(0);
    setPlaying(true);
  }

  return (
    <section aria-label="Synchronized timeline overview" className="synchronized-timeline-panel">
      <header className="synchronized-timeline-head">
        <div>
          <p><Layers3 size={13} /> TIMING OVERVIEW</p>
          <h2>Every cue resolves on one shared timeline.</h2>
          <span>Video, reference and target text, prosody, and output speech are read as a synchronized task overview.</span>
        </div>
        <strong>GLOBAL TASK VIEW</strong>
      </header>
      <div className="synchronized-timeline-board">
        <div className="synchronized-timeline-toolbar">
          <button aria-label={playing ? "Pause illustrated timeline" : "Play illustrated timeline"} className={`synchronized-timeline-play${playing ? " is-playing" : ""}`} onClick={togglePlayback} type="button">
            {pulseId ? <span aria-hidden="true" className="synchronized-timeline-play-pulse" key={pulseId} /> : null}
            {playing ? <CirclePause fill="currentColor" size={17} /> : <CirclePlay fill="currentColor" size={17} />}
          </button>
          <span>{timecode}</span>
          <strong>ONE SYNCHRONIZED TIMELINE</strong>
          <span className="synchronized-timeline-status">TASK OVERVIEW</span>
        </div>
        <div className="synchronized-timeline-tracks">
          <TimelineTrack label="VIDEO"><div className="synchronized-filmstrip">{Array.from({ length: FILMSTRIP_FRAME_COUNT }, (_, index) => <img alt="" key={index} src="/atlas/demo/scene-v1.png" />)}</div></TimelineTrack>
          <TimelineTrack label="SUBTITLES" variant="subtitles"><div aria-label="Target subtitle cue: The scene changes how a line should sound." className="synchronized-subtitles">{TASK_ILLUSTRATION_SUBTITLE_TOKENS.map((token) => <span key={token}>{token}</span>)}</div></TimelineTrack>
          <TimelineTrack label="PHONEMES"><div className="synchronized-ipa">{TASK_ILLUSTRATION_IPA.map((token) => <span key={token}>{token}</span>)}</div></TimelineTrack>
          <TimelineTrack label="PROSODY"><div className="synchronized-signal-label">ILLUSTRATED PITCH + ENERGY</div><ProsodyCurve /></TimelineTrack>
          <TimelineTrack label="OUTPUT" variant="output"><div className="synchronized-signal-label">TARGET SPEECH WAVEFORM</div><OutputWaveform peaks={ILLUSTRATED_TARGET_SPEECH} /></TimelineTrack>
        </div>
        <input aria-label="Illustrated task time" className="synchronized-timeline-range" max="100" min="0" onChange={(event) => setProgress(Number(event.target.value))} type="range" value={progress} />
        <span className="synchronized-timeline-playhead" style={{ left: `calc(94px + (100% - 114px) * ${progress / 100})` }} />
      </div>
      <footer>ONE SYNCHRONIZED TIMELINE · ILLUSTRATED TASK OVERVIEW</footer>
    </section>
  );
}

function TimelineTrack({ children, label, variant }: { children: React.ReactNode; label: string; variant?: "output" | "subtitles" }) {
  return <div className={`synchronized-timeline-track${variant ? ` is-${variant}` : ""}`}><span>{label}</span><div>{children}</div></div>;
}

function ProsodyCurve() {
  return <svg aria-label="Illustrated pitch and energy" className="synchronized-prosody" preserveAspectRatio="none" viewBox="0 0 600 42"><path d="M0 30 C30 29 44 8 72 18 S110 32 140 20 S180 4 205 16 S244 32 270 21 S320 11 345 20 S385 32 412 16 S452 6 480 19 S530 30 600 12" /><path className="synchronized-energy" d="M0 34 C45 24 72 33 110 26 S175 34 220 16 S285 31 332 24 S405 36 450 18 S530 31 600 20" /></svg>;
}

function OutputWaveform({ peaks }: { peaks: number[] }) {
  return <svg aria-label="Target speech waveform" className="synchronized-output-waveform" data-illustration="target-speech-waveform" preserveAspectRatio="none" viewBox="0 0 100 100">{peaks.map((peak, index) => {
    const x = (index / Math.max(1, peaks.length - 1)) * 100;
    const y = 50 - peak * 42;
    return <polyline key={x} points={`${x},${y} ${x},${100 - y}`} strokeLinecap="round" />;
  })}</svg>;
}
