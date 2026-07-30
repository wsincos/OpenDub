import {
  AudioLines,
  ChevronRight,
  CirclePause,
  CirclePlay,
  Film,
  Layers3,
  RotateCcw,
  Sparkles,
  Subtitles,
  Volume2,
} from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { SynchronizedTimelinePanel } from "./SynchronizedTimelinePanel";
import { TaskIllustrationPanel, type TaskInputId } from "./TaskIllustrationPanel";
import { ILLUSTRATED_REFERENCE_CONTOUR, ILLUSTRATED_TARGET_SPEECH } from "./illustrated-task-signals";
import "./vtts-task-stage.css";

type FlowPhase = "idle" | "video-cues" | "text-timing" | "reference-identity" | "method-resolve" | "outputs";

const phases: Array<{ id: Exclude<FlowPhase, "idle">; label: string }> = [
  { id: "video-cues", label: "Visual timing cues" },
  { id: "text-timing", label: "Text timing" },
  { id: "reference-identity", label: "Reference identity" },
  { id: "method-resolve", label: "Complete method" },
  { id: "outputs", label: "Target output" },
];

const ipaTokens = ["ðə", "siːn", "ˈtʃeɪn.dʒɪz", "haʊ", "ə", "laɪn", "ʃʊd", "saʊnd"];

export function VttsTaskStagePage() {
  const [flowPhase, setFlowPhase] = useState<FlowPhase>("idle");
  const [running, setRunning] = useState(false);
  const [selectedInput, setSelectedInput] = useState<TaskInputId>("video");
  const search = new URLSearchParams(window.location.search);
  const compactFlowOverview = search.get("capture") === "overview";

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
    const tour = search.get("tour");
    if (tour === "flow") {
      setFlowPhase("video-cues");
      setRunning(true);
      return;
    }
    if (tour === "cues") {
      const timer = window.setTimeout(() => document.querySelector(".task-illustration")?.scrollIntoView({ block: "center" }), 120);
      return () => window.clearTimeout(timer);
    }
    if (tour === "timeline") {
      const timer = window.setTimeout(() => document.querySelector(".synchronized-timeline-panel")?.scrollIntoView({ block: "center" }), 120);
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

  function inspectInput(input: TaskInputId, phase: Exclude<FlowPhase, "idle">) {
    setSelectedInput(input);
    setFlowPhase(phase);
  }

  return (
    <main className="vtts-page" aria-label="OpenDub VTTS Task Stage">
      <section className="vtts-intro">
        <div>
          <p className="vtts-kicker"><Sparkles size={13} /> OPEN-SOURCE MULTIMODAL INTELLIGENT VIDEO DUBBING PLATFORM</p>
          <h1>Video dubbing turns a scene into speech.</h1>
          <p>Video, text, and authorized reference speech are not interchangeable prompts. Text can provide both reference and target timing context; a complete dubbing method has to hold timing, identity, and expression constraints together.</p>
        </div>
        <div className="vtts-intro-protocol"><span>VTTS / TASK STAGE</span><strong>3 inputs → 1 complete method → 2 outputs</strong><small>Interactive explanation · no generation claim</small></div>
      </section>

      <section className={`vtts-flow ${running ? "is-running" : ""}${compactFlowOverview ? " vtts-flow--capture-overview" : ""}`} data-phase={flowPhase} aria-label="Video text to speech task flow">
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
          <button aria-label="Silent video input" aria-pressed={selectedInput === "video"} className={`flow-input flow-input-video${selectedInput === "video" ? " is-selected" : ""}`} onClick={() => inspectInput("video", "video-cues")} type="button">
            <span className="flow-input-header"><Film size={14} /> SILENT VIDEO <i>01</i></span>
            <span aria-label="Five-frame silent video filmstrip" className="filmstrip">
              {Array.from({ length: 5 }).map((_, index) => <span className="filmstrip-frame" key={index}><img alt="" src="/showcases/v2/human-0/poster.jpg" style={{ objectPosition: `${39 + index * 5}% 42%` }} /><i aria-hidden="true">{String(index + 1).padStart(2, "0")}</i></span>)}
            </span>
            <strong>Visual timing packets</strong><small>Face · lip · environment</small>
          </button>
          <button aria-label="Text input" aria-pressed={selectedInput === "text"} className={`flow-input flow-input-text${selectedInput === "text" ? " is-selected" : ""}`} onClick={() => inspectInput("text", "text-timing")} type="button">
            <span className="flow-input-header"><Subtitles size={14} /> TEXT <i>02</i></span>
            <strong>The scene changes how a line should sound.</strong>
            <span className="flow-ipa">{ipaTokens.slice(0, 5).map((token) => <i key={token}>{token}</i>)}</span>
            <small>Reference + target text timing</small>
          </button>
          <button aria-label="Authorized reference speech input" aria-pressed={selectedInput === "reference"} className={`flow-input flow-input-reference${selectedInput === "reference" ? " is-selected" : ""}`} onClick={() => inspectInput("reference", "reference-identity")} type="button">
            <span className="flow-input-header"><AudioLines size={14} /> AUTHORIZED REFERENCE SPEECH <i>03</i></span>
            <Waveform illustration="reference-contour" label="Reference contour" peaks={ILLUSTRATED_REFERENCE_CONTOUR} tone="voice" />
            <strong>Identity and style envelope</strong><small>Illustrated contour · no archive audio</small>
          </button>
        </div>
        <section className="complete-method" aria-label="Complete dubbing method">
          <p><Layers3 size={14} /> COMPLETE METHOD</p>
          <h2>Constrain the whole performance.</h2>
          <div className="method-lenses"><span>SYNC<br /><b>timing</b></span><span>VOICE<br /><b>identity</b></span><span>STYLE<br /><b>expression</b></span></div>
          <Link to="/methods">Inspect complete methods <ChevronRight size={15} /></Link>
        </section>
        <section className="flow-outputs" aria-label="Task outputs">
          <div className="flow-output flow-output-speech"><span className="flow-input-header"><Volume2 size={14} /> TARGET SPEECH</span><Waveform illustration="target-speech" label="Target speech illustration" peaks={ILLUSTRATED_TARGET_SPEECH} tone="output" /><strong>Research output: speech</strong><small>Task illustration · no fresh run</small></div>
          <div className="flow-output flow-output-video"><span className="flow-input-header"><Film size={14} /> DUBBED VIDEO</span><div className="task-video-frame"><video aria-label="Looping dubbed video preview" autoPlay loop muted playsInline poster="/showcases/v2/human-0/poster.jpg" preload="metadata" src="/showcases/v2/human-0/emodubber.mp4" /></div><strong>Product output: video + speech</strong><small>Task illustration · no fresh run</small></div>
        </section>
      </section>

      <TaskIllustrationPanel activeInput={selectedInput} />
      <SynchronizedTimelinePanel />
    </main>
  );
}

function FlowPacket({ active, color, delay = "0s", path }: { active: boolean; color: string; delay?: string; path: string }) {
  return <circle className="flow-packet" fill={color} r="4" visibility={active ? "visible" : "hidden"}><animateMotion begin={active ? delay : "indefinite"} dur="1.1s" path={path} repeatCount="indefinite" /></circle>;
}

function Waveform({ illustration, label, peaks, tone }: { illustration: string; label: string; peaks: number[]; tone: "voice" | "output" }) {
  const points = peaks.map((value, index) => {
    const x = (index / Math.max(1, peaks.length - 1)) * 100;
    const y = 50 - value * 42;
    return `${x},${y} ${x},${100 - y}`;
  });
  return <svg aria-label={label} className={`real-waveform ${tone}`} data-illustration={illustration} preserveAspectRatio="none" viewBox="0 0 100 100">{points.map((point, index) => <polyline key={index} points={point} />)}</svg>;
}
