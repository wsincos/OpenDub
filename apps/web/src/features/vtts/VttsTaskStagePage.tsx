import {
  AudioLines,
  ChevronRight,
  CirclePause,
  CirclePlay,
  Film,
  Layers3,
  RotateCcw,
  ScanFace,
  Sparkles,
  Subtitles,
  Volume2,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

import { ExampleGalleryPage } from "../showcases/ExampleGalleryPage";
import { publicShowcaseUrl } from "../../content/showcases";
import "./vtts-task-stage.css";

type FlowPhase = "idle" | "video-cues" | "text-timing" | "reference-identity" | "method-resolve" | "outputs";
type CueLayer = "face" | "lip" | "environment";
type AudioFeature = {
  waveform_peaks: number[];
  times_seconds: number[];
  energy: number[];
  f0_hz: Array<number | null>;
};

const phases: Array<{ id: Exclude<FlowPhase, "idle">; label: string }> = [
  { id: "video-cues", label: "Visual timing cues" },
  { id: "text-timing", label: "Target text timing" },
  { id: "reference-identity", label: "Reference identity" },
  { id: "method-resolve", label: "Complete method" },
  { id: "outputs", label: "Target output" },
];

const ipaTokens = ["ðə", "siːn", "ˈtʃeɪn.dʒɪz", "haʊ", "ə", "laɪn", "ʃʊd", "saʊnd"];

export function VttsTaskStagePage() {
  const [flowPhase, setFlowPhase] = useState<FlowPhase>("idle");
  const [running, setRunning] = useState(false);
  const [activeCue, setActiveCue] = useState<CueLayer>("face");
  const [timelineProgress, setTimelineProgress] = useState(38);
  const taskVideo = useRef<HTMLVideoElement>(null);
  const feature = useAudioFeature("/showcases/v2/human-0/features/gt.json");

  useEffect(() => {
    if (!running) return undefined;
    const timers = phases.map((phase, index) => window.setTimeout(() => setFlowPhase(phase.id), index * 1150));
    const complete = window.setTimeout(() => setRunning(false), phases.length * 1150 + 300);
    return () => {
      timers.forEach((timer) => window.clearTimeout(timer));
      window.clearTimeout(complete);
    };
  }, [running]);

  useEffect(() => {
    const tour = new URLSearchParams(window.location.search).get("tour");
    if (tour === "flow") {
      setFlowPhase("video-cues");
      setRunning(true);
      return;
    }
    if (tour === "cues") {
      const timer = window.setTimeout(() => {
        setActiveCue("environment");
        document.querySelector(".cue-microscope")?.scrollIntoView({ block: "center" });
      }, 120);
      return () => window.clearTimeout(timer);
    }
    if (tour === "timeline") {
      const timer = window.setTimeout(() => document.querySelector(".sync-timeline")?.scrollIntoView({ block: "center" }), 120);
      return () => window.clearTimeout(timer);
    }
    return undefined;
  }, []);

  function toggleFlow() {
    if (running) {
      setRunning(false);
      return;
    }
    setFlowPhase("video-cues");
    setRunning(true);
  }

  function resetFlow() {
    setRunning(false);
    setFlowPhase("idle");
  }

  function updateTimeline(progress: number) {
    setTimelineProgress(progress);
    if (taskVideo.current && Number.isFinite(taskVideo.current.duration)) {
      taskVideo.current.currentTime = (taskVideo.current.duration * progress) / 100;
    }
  }

  return (
    <main className="vtts-page" aria-label="OpenDub VTTS Task Stage">
      <section className="vtts-intro">
        <div>
          <p className="vtts-kicker"><Sparkles size={13} /> OPEN-SOURCE MULTIMODAL INTELLIGENT VIDEO DUBBING PLATFORM</p>
          <h1>Video dubbing turns a scene into speech.</h1>
          <p>Video, target text, and authorized reference speech are not interchangeable prompts. A complete dubbing method has to hold their timing, identity, and expression constraints together.</p>
        </div>
        <div className="vtts-intro-protocol"><span>VTTS / TASK STAGE</span><strong>3 inputs → 1 complete method → 2 outputs</strong><small>Interactive explanation · no generation claim</small></div>
      </section>

      <section className={`vtts-flow ${running ? "is-running" : ""}`} data-phase={flowPhase} aria-label="Video text to speech task flow">
        <div className="flow-toolbar">
          <span aria-live="polite" className="flow-state">{flowPhase === "idle" ? "Ready to inspect task" : phases.find((phase) => phase.id === flowPhase)?.label}</span>
          <div>
            <button aria-label={running ? "Pause task flow" : "Play task flow"} className="flow-control" onClick={toggleFlow} type="button">{running ? <CirclePause size={17} /> : <CirclePlay size={17} />}</button>
            <button aria-label="Reset task flow" className="flow-control" onClick={resetFlow} type="button"><RotateCcw size={15} /></button>
          </div>
        </div>
        <svg aria-hidden="true" className="flow-wiring" preserveAspectRatio="none" viewBox="0 0 1200 540">
          <path className="flow-path path-video" d="M270 133 H488 Q520 133 546 238 H648" />
          <path className="flow-path path-text" d="M270 270 H648" />
          <path className="flow-path path-reference" d="M270 407 H488 Q520 407 546 302 H648" />
          <path className="flow-path path-output" d="M810 270 H942" />
          <path className="flow-path path-video-output" d="M810 286 H888 Q912 286 942 388" />
          <FlowPacket active={running} color="#72c9e9" path="M270 133 H488 Q520 133 546 238 H648" />
          <FlowPacket active={running} color="#f0b967" delay=".18s" path="M270 270 H648" />
          <FlowPacket active={running} color="#a795eb" delay=".34s" path="M270 407 H488 Q520 407 546 302 H648" />
          <FlowPacket active={running} color="#81d1a5" delay=".62s" path="M810 270 H942" />
          <FlowPacket active={running} color="#81d1a5" delay=".82s" path="M810 286 H888 Q912 286 942 388" />
        </svg>
        <div className="flow-inputs">
          <button aria-label="Silent video input" className="flow-input flow-input-video" onClick={() => setActiveCue("face")} type="button">
            <span className="flow-input-header"><Film size={14} /> SILENT VIDEO <i>01</i></span>
            <span className="filmstrip">
              {Array.from({ length: 5 }).map((_, index) => <img alt="" key={index} src="/showcases/v2/human-0/poster.jpg" style={{ objectPosition: `${39 + index * 5}% 40%` }} />)}
            </span>
            <strong>Visual timing packets</strong><small>Face · lip · environment</small>
          </button>
          <button aria-label="Target text input" className="flow-input flow-input-text" onClick={() => setFlowPhase("text-timing")} type="button">
            <span className="flow-input-header"><Subtitles size={14} /> TARGET TEXT <i>02</i></span>
            <strong>The scene changes how a line should sound.</strong>
            <span className="flow-ipa">{ipaTokens.slice(0, 5).map((token) => <i key={token}>{token}</i>)}</span>
            <small>Illustrated IPA timing notation</small>
          </button>
          <button aria-label="Authorized reference speech input" className="flow-input flow-input-reference" onClick={() => setFlowPhase("reference-identity")} type="button">
            <span className="flow-input-header"><AudioLines size={14} /> AUTHORIZED REFERENCE SPEECH <i>03</i></span>
            <Waveform feature={feature} label="Reference contour" tone="voice" />
            <strong>Identity and style envelope</strong><small>Feature source disclosed below</small>
          </button>
        </div>
        <section className="complete-method" aria-label="Complete dubbing method">
          <p><Layers3 size={14} /> COMPLETE METHOD</p>
          <h2>Constrain the whole performance.</h2>
          <div className="method-lenses"><span>SYNC<br /><b>timing</b></span><span>VOICE<br /><b>identity</b></span><span>STYLE<br /><b>expression</b></span></div>
          <Link to="/methods">Inspect complete methods <ChevronRight size={15} /></Link>
        </section>
        <section className="flow-outputs" aria-label="Task outputs">
          <div className="flow-output flow-output-speech"><span className="flow-input-header"><Volume2 size={14} /> TARGET SPEECH</span><Waveform feature={feature} label="Target speech illustration" tone="output" /><strong>Research output: speech</strong><small>Task illustration · no fresh run</small></div>
          <div className="flow-output flow-output-video"><span className="flow-input-header"><Film size={14} /> DUBBED VIDEO</span><div className="task-video-frame"><video muted playsInline poster="/showcases/v2/human-0/poster.jpg" preload="metadata" ref={taskVideo} src="/showcases/v2/human-0/gt.mp4" /><span>CASE VISUAL / ARCHIVED</span></div><strong>Product output: video + speech</strong><small>Task illustration · no fresh run</small></div>
        </section>
      </section>

      <section className="cue-microscope" aria-label="Synchronized cue microscope">
        <div className="cue-copy"><p className="vtts-kicker"><ScanFace size={13} /> CUE MICROSCOPE</p><h2>One scene constrains more than lip timing.</h2><p>OpenDub exposes understandable visual observations. These overlays are inspection cues, not a claim to expose unpublished internal model tensors.</p><div className="cue-controls">{(["face", "lip", "environment"] as CueLayer[]).map((cue) => <button aria-label={`${cue[0].toUpperCase()}${cue.slice(1)} cue`} aria-pressed={activeCue === cue} className={activeCue === cue ? "is-active" : ""} key={cue} onClick={() => setActiveCue(cue)} type="button">{cue === "face" ? "Face" : cue === "lip" ? "Lip" : "Environment"}</button>)}</div></div>
        <div className={`cue-visual cue-${activeCue}`}>
          <img alt="Archived human portrait case visual" src="/showcases/v2/human-0/poster.jpg" />
          <span className="cue-box face-box">FACE / expression</span><span className="cue-box lip-box">LIP / timing</span><span className="cue-box environment-box">ENV / scene pulse</span><span className="cue-time">00:01.14</span>
        </div>
        <div className="cue-inspector"><span className="cue-inspector-index">0{["face", "lip", "environment"].indexOf(activeCue) + 1}</span><h3>{activeCue === "face" ? "Face" : activeCue === "lip" ? "Lip" : "Environment"}</h3><p>{activeCue === "face" ? "Expression changes can be checked as an interpretable cue for energy and pitch context." : activeCue === "lip" ? "Mouth opening and closure provide local timing constraints around speech units." : "Scene rhythm, shot context, and global motion provide inspectable global context."}</p><small>Observation source: visual case frame</small></div>
      </section>

      <section className="sync-timeline" aria-label="Synchronized task timeline">
        <div className="timeline-head"><div><p className="vtts-kicker"><Layers3 size={13} /> SHARED TIMEBASE</p><h2>Signals meet at one playhead.</h2></div><div className="feature-citation"><span>Feature source: human-0 / GT audio · IPA track: task notation</span><figure><img alt="Actual log-mel feature from human-0 ground truth" src="/showcases/v2/human-0/features/gt.mel.png" /><figcaption>LOG-MEL / DERIVED FEATURE</figcaption></figure></div></div>
        <div className="timeline-ruler"><span>00:00</span><span>00:01</span><span>00:02</span><span>00:03</span></div>
        <TimelineTrack label="VIDEO"><div className="timeline-filmstrip">{Array.from({ length: 12 }).map((_, index) => <img alt="" key={index} src="/showcases/v2/human-0/poster.jpg" style={{ objectPosition: `${32 + index * 4}% 40%` }} />)}</div></TimelineTrack>
        <TimelineTrack label="IPA"><div className="timeline-ipa">{ipaTokens.map((token, index) => <span key={`${token}-${index}`} style={{ width: `${100 / ipaTokens.length - 1}%` }}>{token}</span>)}</div></TimelineTrack>
        <TimelineTrack label="CUES"><div className="timeline-cues"><span className="cue-face-bar">Face</span><span className="cue-lip-bar">Lip</span><span className="cue-environment-bar">Environment</span></div></TimelineTrack>
        <TimelineTrack label="PROSODY"><Prosody feature={feature} /></TimelineTrack>
        <TimelineTrack label="SPEECH"><Waveform feature={feature} label="Speech waveform" tone="output" /></TimelineTrack>
        <input aria-label="Synchronized task time" max="100" min="0" onChange={(event) => updateTimeline(Number(event.target.value))} type="range" value={timelineProgress} />
        <span className="timeline-playhead" style={{ left: `calc(112px + (100% - 132px) * ${timelineProgress / 100})` }} />
      </section>

      <ExampleGalleryPage embedded />
    </main>
  );
}

function TimelineTrack({ children, label }: { children: React.ReactNode; label: string }) {
  return <div className="sync-track"><span>{label}</span><div>{children}</div></div>;
}

function FlowPacket({ active, color, delay = "0s", path }: { active: boolean; color: string; delay?: string; path: string }) {
  return <circle className="flow-packet" fill={color} r="4" visibility={active ? "visible" : "hidden"}><animateMotion begin={active ? delay : "indefinite"} dur="1.1s" path={path} repeatCount="indefinite" /></circle>;
}

function Waveform({ feature, label, tone }: { feature: AudioFeature | null; label: string; tone: "voice" | "output" }) {
  const values = feature?.waveform_peaks ?? [];
  if (!values.length) return <div aria-label={label} className={`signal-placeholder ${tone}`}>Awaiting approved audio feature</div>;
  const points = values.map((value, index) => {
    const x = (index / Math.max(1, values.length - 1)) * 100;
    const y = 50 - value * 42;
    return `${x},${y} ${x},${100 - y}`;
  });
  return <svg aria-label={label} className={`real-waveform ${tone}`} preserveAspectRatio="none" viewBox="0 0 100 100">{points.map((point, index) => <polyline key={index} points={point} />)}</svg>;
}

function Prosody({ feature }: { feature: AudioFeature | null }) {
  const values = feature?.f0_hz ?? [];
  const voiced = values.filter((value): value is number => value !== null);
  if (!voiced.length) return <div className="signal-placeholder output">Awaiting approved F0 + energy feature</div>;
  const minimum = Math.min(...voiced);
  const maximum = Math.max(...voiced);
  const path = values.map((value, index) => {
    const x = (index / Math.max(1, values.length - 1)) * 100;
    const normalized = value === null ? .5 : (value - minimum) / Math.max(1, maximum - minimum);
    return `${x},${84 - normalized * 62}`;
  }).join(" ");
  return <svg aria-label="Actual F0 and energy feature" className="prosody-graph" preserveAspectRatio="none" viewBox="0 0 100 100"><polyline points={path} /><polyline className="energy" points={feature?.energy.map((value, index) => `${(index / Math.max(1, (feature?.energy.length ?? 1) - 1)) * 100},${94 - value * 34}`).join(" ")} /></svg>;
}

function useAudioFeature(path: string): AudioFeature | null {
  const [feature, setFeature] = useState<AudioFeature | null>(null);
  useEffect(() => {
    let active = true;
    if (import.meta.env.MODE === "test") return () => { active = false; };
    if (typeof fetch !== "function") return () => { active = false; };
    fetch(path).then((response) => response.ok ? response.json() : null).then((payload: AudioFeature | null) => { if (active) setFeature(payload); }).catch(() => { if (active) setFeature(null); });
    return () => { active = false; };
  }, [path]);
  return feature;
}
