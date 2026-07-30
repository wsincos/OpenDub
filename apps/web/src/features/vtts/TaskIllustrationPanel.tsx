import { AudioLines, Check, Film, ScanFace, Subtitles } from "lucide-react";
import { useState } from "react";

import { ILLUSTRATED_REFERENCE_CONTOUR } from "./illustrated-task-signals";
import "./task-illustration-panel.css";

export type TaskInputId = "video" | "text" | "reference";

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

export const TASK_ILLUSTRATION_SUBTITLE_TOKENS = [
  "The",
  "scene",
  "changes",
  "how",
  "a",
  "line",
  "should",
  "sound.",
] as const;

export function TaskIllustrationPanel({ activeInput = "video" }: { activeInput?: TaskInputId }) {
  const [faceVisible, setFaceVisible] = useState(true);
  const [lipVisible, setLipVisible] = useState(true);
  const [environmentVisible, setEnvironmentVisible] = useState(true);
  const metadata = illustrationMetadata(activeInput);

  return (
    <section aria-label="Task illustration" aria-live="polite" className={`task-illustration is-${activeInput}`}>
      <header className="task-illustration-head">
        <div>
          <p className="task-illustration-kicker">{metadata.icon} TASK ILLUSTRATION · {metadata.kicker}</p>
          <h2>{metadata.title}</h2>
          <p>{metadata.description}</p>
        </div>
        <span className="task-illustration-boundary">{metadata.boundary}</span>
      </header>
      {activeInput === "video" ? (
        <div className="task-illustration-body task-illustration-scene">
          <div className="task-illustration-frame">
            <img alt="Illustrative woman in a concept video-dubbing scene" src="/atlas/demo/scene-v1.png" />
            {faceVisible ? <span className="task-illustration-roi task-illustration-face"><ScanFace size={13} /> Face affect</span> : null}
            {lipVisible ? <span className="task-illustration-roi task-illustration-lip">Lip motion</span> : null}
            {environmentVisible ? <span className="task-illustration-roi task-illustration-environment">Environment</span> : null}
            <span className="task-illustration-time">00:01.2</span>
          </div>
          <div className="task-illustration-copy">
            <p>VISUAL OBSERVATION</p>
            <h3>Inspect face, lip, and scene context separately.</h3>
            <span>These overlays are explanatory controls, not unexposed model tensors.</span>
            <div className="task-illustration-controls">
              <button aria-label={faceVisible ? "Hide face overlay" : "Show face overlay"} className={faceVisible ? "is-enabled" : ""} onClick={() => setFaceVisible((visible) => !visible)} type="button"><Check size={14} /> Face</button>
              <button aria-label={lipVisible ? "Hide lip overlay" : "Show lip overlay"} className={lipVisible ? "is-enabled" : ""} onClick={() => setLipVisible((visible) => !visible)} type="button"><Check size={14} /> Lip</button>
              <button aria-label={environmentVisible ? "Hide environment overlay" : "Show environment overlay"} className={environmentVisible ? "is-enabled" : ""} onClick={() => setEnvironmentVisible((visible) => !visible)} type="button"><Check size={14} /> Environment</button>
            </div>
          </div>
        </div>
      ) : null}
      {activeInput === "text" ? <TextIllustration /> : null}
      {activeInput === "reference" ? <ReferenceAudioIllustration /> : null}
      <footer>TASK ILLUSTRATION · {metadata.footer}</footer>
    </section>
  );
}

function illustrationMetadata(activeInput: TaskInputId) {
  if (activeInput === "text") {
    return {
      boundary: "ILLUSTRATED TASK COPY / 02",
      description: "A shared text view keeps reference context and the target line legible before their linguistic timing is aligned.",
      footer: "ILLUSTRATED TEXT CONTEXT",
      icon: <Subtitles size={13} />,
      kicker: "TEXT INPUT",
      title: "Reference and target text share one timing view.",
    };
  }
  if (activeInput === "reference") {
    return {
      boundary: "ILLUSTRATED CONDITION / 03",
      description: "Reference audio supplies a stable identity and style condition, alongside the visual and textual requirements of the task.",
      footer: "AUTHORIZED REFERENCE CONDITION",
      icon: <AudioLines size={13} />,
      kicker: "REFERENCE AUDIO",
      title: "Reference audio anchors identity and style.",
    };
  }
  return {
    boundary: "SILENT VIDEO / 01",
    description: "A task illustration shows how facial affect, local lip motion, and scene context can be inspected before they are resolved with text and reference audio.",
    footer: "CONCEPT SCENE · NO CASE AUDIO OR TRANSCRIPT",
    icon: <ScanFace size={13} />,
    kicker: "CONCEPT SCENE",
    title: "One scene carries several timing cues.",
  };
}

function TextIllustration() {
  return (
    <div className="task-illustration-body task-illustration-text">
      <div className="task-illustration-script">
        <p><Subtitles size={14} /> TEXT CONTEXT</p>
        <div className="task-illustration-script-line is-reference"><span>REFERENCE TEXT</span><blockquote>“A quiet scene can still carry intent.”</blockquote></div>
        <div className="task-illustration-script-line is-target"><span>TARGET TEXT</span><blockquote>“The scene changes how a line should sound.”</blockquote></div>
        <small className="task-illustration-illustrative-note">ILLUSTRATED / NO ARCHIVE AUDIO OR TRANSCRIPT</small>
      </div>
      <div className="task-illustration-copy task-illustration-timing-copy">
        <p>LINGUISTIC TIMING</p>
        <h3>Read the context, then align the line.</h3>
        <span>Reference and target text are shown together so their semantic context and phoneme-level timing can be inspected as one condition.</span>
        <div aria-label="Illustrative target phoneme intervals" className="task-illustration-phoneme-grid">
          {TASK_ILLUSTRATION_IPA.map((token) => <i key={token}>{token}</i>)}
        </div>
      </div>
    </div>
  );
}

function ReferenceAudioIllustration() {
  return (
    <div className="task-illustration-body task-illustration-audio">
      <div className="task-illustration-audio-visual">
        <div className="task-illustration-audio-mark"><AudioLines size={26} /><span>REF<br />AUDIO</span></div>
        <div className="task-illustration-waveform-wrap">
          <span>IDENTITY + STYLE CONTOUR</span>
          <ReferenceWaveform values={ILLUSTRATED_REFERENCE_CONTOUR} />
        </div>
      </div>
      <div className="task-illustration-copy">
        <p>AUTHORIZED REFERENCE AUDIO</p>
        <h3>Carry identity without replacing the performance.</h3>
        <span>The reference condition contributes speaker identity and expressive style. The final delivery still follows the selected video and target text.</span>
        <div className="task-illustration-attributes"><span>VOICE IDENTITY</span><span>STYLE ENVELOPE</span><span>AUTHORIZED SOURCE</span></div>
        <small className="task-illustration-illustrative-note">ILLUSTRATED / NO ARCHIVE AUDIO OR TRANSCRIPT</small>
      </div>
    </div>
  );
}

function ReferenceWaveform({ values }: { values: number[] }) {
  return (
    <svg aria-label="Reference identity waveform" className="task-illustration-reference-waveform" data-illustration="reference-identity" preserveAspectRatio="none" viewBox="0 0 100 100">
      {values.map((value, index) => {
        const x = (index / Math.max(1, values.length - 1)) * 100;
        const y = 50 - value * 42;
        return <polyline key={index} points={`${x},${y} ${x},${100 - y}`} />;
      })}
    </svg>
  );
}
