import { Check, CirclePause, CirclePlay, ScanFace, Waves } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import "./task-illustration-panel.css";

export const TASK_ILLUSTRATION_IPA = [
  "ðə",
  "siːn",
  "ˈtʃeɪn.dʒɪz",
  "haʊ",
  "ə",
  "laɪn",
  "ʃʊd",
  "saʊnd",
] as const;

const WAVEFORM_BARS = [18, 32, 14, 47, 66, 35, 54, 78, 28, 61, 43, 20, 58, 72, 38, 51, 82, 31, 19, 46, 69, 37, 57, 24, 64, 41, 17, 53, 74, 34, 59, 23, 45, 68, 29, 49];

export function TaskIllustrationPanel() {
  const [faceVisible, setFaceVisible] = useState(true);
  const [lipVisible, setLipVisible] = useState(true);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(42);

  useEffect(() => {
    if (!playing) return undefined;
    const interval = window.setInterval(() => setProgress((current) => (current >= 100 ? 0 : current + 1)), 80);
    return () => window.clearInterval(interval);
  }, [playing]);

  const timecode = useMemo(() => {
    const seconds = (progress / 100) * 3;
    return `00:0${Math.floor(seconds)}.${Math.floor((seconds % 1) * 10)}`;
  }, [progress]);

  return (
    <section className="task-illustration" aria-label="Illustrated synchronized task timeline">
      <header className="task-illustration-head">
        <div>
          <p className="task-illustration-kicker"><ScanFace size={13} /> TASK ILLUSTRATION · CONCEPT SCENE</p>
          <h2>One scene carries several timing cues.</h2>
          <p>A task illustration shows how facial affect and local lip motion can be inspected alongside text timing and prosody.</p>
        </div>
        <span className="task-illustration-boundary">NO CASE AUDIO OR TRANSCRIPT</span>
      </header>

      <div className="task-illustration-scene">
        <div className="task-illustration-frame">
          <img alt="Illustrative woman in a concept video-dubbing scene" src="/atlas/demo/scene-v1.png" />
          {faceVisible ? <span className="task-illustration-roi task-illustration-face"><ScanFace size={13} /> Face affect</span> : null}
          {lipVisible ? <span className="task-illustration-roi task-illustration-lip">Lip motion</span> : null}
          <span className="task-illustration-time">{timecode}</span>
        </div>
        <div className="task-illustration-copy">
          <p>VISUAL OBSERVATION</p>
          <h3>Inspect face and lip timing separately.</h3>
          <span>These overlays are explanatory controls, not unexposed model tensors.</span>
          <div className="task-illustration-controls">
            <button aria-label={faceVisible ? "Hide face overlay" : "Show face overlay"} className={faceVisible ? "is-enabled" : ""} onClick={() => setFaceVisible((visible) => !visible)} type="button"><Check size={14} /> Face</button>
            <button aria-label={lipVisible ? "Hide lip overlay" : "Show lip overlay"} className={lipVisible ? "is-enabled" : ""} onClick={() => setLipVisible((visible) => !visible)} type="button"><Check size={14} /> Lip</button>
          </div>
        </div>
      </div>

      <div className="task-illustration-timeline">
        <div className="task-illustration-toolbar">
          <button aria-label={playing ? "Pause illustrated timeline" : "Play illustrated timeline"} className="task-illustration-play" onClick={() => setPlaying((current) => !current)} type="button">
            {playing ? <CirclePause fill="currentColor" size={17} /> : <CirclePlay fill="currentColor" size={17} />}
          </button>
          <span>{timecode}</span>
          <strong>ONE SYNCHRONIZED TIMELINE</strong>
          <span className="task-illustration-status">TASK ILLUSTRATION</span>
        </div>
        <div className="task-illustration-tracks">
          <TimelineTrack label="VIDEO"><div className="task-illustration-filmstrip">{Array.from({ length: 12 }, (_, index) => <img alt="" key={index} src="/atlas/demo/scene-v1.png" style={{ objectPosition: `${33 + index * 3}% center` }} />)}</div></TimelineTrack>
          <TimelineTrack label="PHONEMES"><div className="task-illustration-ipa">{TASK_ILLUSTRATION_IPA.map((token) => <span key={token}>{token}</span>)}</div></TimelineTrack>
          <TimelineTrack label="PROSODY"><div className="task-illustration-signal-label">ILLUSTRATED PITCH + ENERGY</div><ProsodyCurve /></TimelineTrack>
          <TimelineTrack label="OUTPUT"><div className="task-illustration-signal-label">ILLUSTRATED TARGET SPEECH</div><WaveformBars /></TimelineTrack>
        </div>
        <input aria-label="Illustrated task time" className="task-illustration-range" max="100" min="0" onChange={(event) => setProgress(Number(event.target.value))} type="range" value={progress} />
        <span className="task-illustration-playhead" style={{ left: `calc(104px + (100% - 126px) * ${progress / 100})` }} />
      </div>
      <footer>TASK ILLUSTRATION · NO CASE AUDIO OR TRANSCRIPT</footer>
    </section>
  );
}

function TimelineTrack({ children, label }: { children: React.ReactNode; label: string }) {
  return <div className="task-illustration-track"><span>{label}</span><div>{children}</div></div>;
}

function ProsodyCurve() {
  return <svg aria-label="Illustrated pitch and energy" className="task-illustration-prosody" preserveAspectRatio="none" viewBox="0 0 600 42"><path d="M0 30 C30 29 44 8 72 18 S110 32 140 20 S180 4 205 16 S244 32 270 21 S320 11 345 20 S385 32 412 16 S452 6 480 19 S530 30 600 12" /><path className="task-illustration-energy" d="M0 34 C45 24 72 33 110 26 S175 34 220 16 S285 31 332 24 S405 36 450 18 S530 31 600 20" /></svg>;
}

function WaveformBars() {
  return <div aria-label="Illustrated target speech waveform" className="task-illustration-waveform"><Waves size={13} />{WAVEFORM_BARS.map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}</div>;
}
