import { useMemo, useState } from "react";
import {
  AudioLines,
  Check,
  ChevronRight,
  CirclePlay,
  Film,
  Focus,
  Gauge,
  Layers3,
  Pause,
  ScanFace,
  Sparkles,
  Type,
  Waves,
} from "lucide-react";
import { Link } from "react-router-dom";

import "./task-explorer.css";

type InputId = "video" | "text" | "voice";
type OutputTab = "speech" | "video";

const phonemes = [
  { value: "ni", start: 0, width: 14 },
  { value: "zhong", start: 17, width: 19 },
  { value: "yu", start: 39, width: 13 },
  { value: "lai", start: 55, width: 16 },
  { value: "le", start: 74, width: 11 },
];

const waveformBars = [14, 22, 12, 28, 41, 19, 35, 52, 27, 62, 40, 24, 47, 55, 31, 21, 44, 65, 38, 22, 18, 42, 57, 33, 20, 47, 29, 17, 36, 50, 25, 14, 32, 46, 24, 11];

export function TaskExplorerPage() {
  const [selectedInput, setSelectedInput] = useState<InputId>("video");
  const [outputTab, setOutputTab] = useState<OutputTab>("speech");
  const [timePercent, setTimePercent] = useState(42);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showFace, setShowFace] = useState(true);
  const [showLip, setShowLip] = useState(true);
  const [formalView, setFormalView] = useState(false);

  const timecode = useMemo(() => `00:0${Math.floor(timePercent / 10)}.${Math.round(timePercent % 10)}`, [timePercent]);

  return (
    <main className="explorer" aria-label="OpenDub Video Dubbing Task Explorer">
      <section className="explorer-intro">
        <div>
          <p className="eyebrow">OPEN DUBBING METHOD ATLAS</p>
          <h1>Video dubbing is not just reading text.</h1>
          <p className="intro-copy">
            A scene, a script, and an authorized reference voice jointly constrain how a character should sound.
          </p>
        </div>
        <button className="formal-toggle" onClick={() => setFormalView((current) => !current)} type="button">
          <Sparkles size={15} />
          {formalView ? "Natural view" : "Formal view"}
        </button>
      </section>

      <section className="task-instrument" aria-label="Video dubbing task instrument">
        <div className="instrument-topline">
          <span>INPUT CONDITIONS</span>
          <span>COMPLETE DUBBING METHOD</span>
          <span>OUTPUT</span>
        </div>

        <div className="task-grid">
          <section className="input-stack" aria-label="Task inputs">
            <InputButton
              active={selectedInput === "video"}
              detail="Scene · Face · Lip"
              icon={<Film size={17} />}
              label="Video input"
              onClick={() => setSelectedInput("video")}
              title="Video"
            />
            <InputButton
              active={selectedInput === "text"}
              detail="Script · Phonemes"
              icon={<Type size={17} />}
              label="Text input"
              onClick={() => setSelectedInput("text")}
              title="Target text"
            />
            <InputButton
              active={selectedInput === "voice"}
              detail="Identity · Voice style"
              icon={<AudioLines size={17} />}
              label="Reference speech input"
              onClick={() => setSelectedInput("voice")}
              title="Reference speech"
            />

            <div className="input-rule" />
            <p className="input-note">
              The three inputs answer different questions: what appears, what is said, and whose voice is heard.
            </p>
          </section>

          <section className="method-stage" aria-label="Dubbing method">
            <div className="method-beam method-beam-a" />
            <div className="method-beam method-beam-b" />
            <div className="method-beam method-beam-c" />
            <div className="method-card">
              <span className="method-status"><span /> METHOD SELECTOR</span>
              <h2>Complete Dubbing Method</h2>
              <p>{formalView ? "A_hat = F_theta(V, X, A_ref, C)" : "Interprets the scene, script, and reference voice together."}</p>
              <div className="method-steps">
                <span><Focus size={14} /> Visual cues</span>
                <span><Gauge size={14} /> Prosody</span>
                <span><Waves size={14} /> Speech</span>
              </div>
              <Link className="method-link" to="/methods"><Layers3 size={15} /> Explore three complete methods <ChevronRight size={15} /></Link>
            </div>
          </section>

          <section className="output-panel" aria-label="Task outputs">
            <div className="output-tabs" role="tablist" aria-label="Task output mode">
              <button
                aria-selected={outputTab === "speech"}
                className={outputTab === "speech" ? "is-active" : ""}
                onClick={() => setOutputTab("speech")}
                role="tab"
                type="button"
              >
                Generated Speech
              </button>
              <button
                aria-selected={outputTab === "video"}
                className={outputTab === "video" ? "is-active" : ""}
                onClick={() => setOutputTab("video")}
                role="tab"
                type="button"
              >
                Dubbed Video
              </button>
            </div>
            {outputTab === "speech" ? <SpeechOutput /> : <DubbedVideoOutput />}
          </section>
        </div>

        <section className="input-inspector" aria-live="polite">
          {selectedInput === "video" ? (
            <div className="video-inspector">
              <div className="scene-frame">
                <img alt="Fictional actor in the OpenDub authorized concept scene" src="/atlas/demo/scene-v1.png" />
                {showFace ? <span className="roi-box face-roi"><ScanFace size={13} /> Face affect</span> : null}
                {showLip ? <span className="roi-box lip-roi">Lip motion</span> : null}
                <span className="frame-label">CONCEPT CASE · 00:04.2</span>
              </div>
              <div className="inspector-copy">
                <p className="panel-label"><Film size={14} /> VIDEO INPUT</p>
                <h2>One scene carries several timing cues.</h2>
                <p>Methods may observe the full scene, facial affect, and local lip movement at different scales.</p>
                <div className="layer-controls">
                  <button className={showFace ? "is-enabled" : ""} onClick={() => setShowFace((value) => !value)} type="button"><Check size={14} /> Face</button>
                  <button className={showLip ? "is-enabled" : ""} onClick={() => setShowLip((value) => !value)} type="button"><Check size={14} /> Lip</button>
                  <span>Illustrative visual overlays</span>
                </div>
              </div>
            </div>
          ) : null}
          {selectedInput === "text" ? (
            <div className="text-inspector">
              <div className="script-copy">
                <p className="panel-label"><Type size={14} /> TARGET TEXT</p>
                <blockquote>“你终于来了。”</blockquote>
                <p>A visible script becomes a sequence of phoneme-level timing constraints.</p>
              </div>
              <div className="phoneme-ruler" aria-label="Illustrative phoneme intervals">
                {phonemes.map((phoneme) => <span key={phoneme.value} style={{ left: `${phoneme.start}%`, width: `${phoneme.width}%` }}>{phoneme.value}</span>)}
              </div>
            </div>
          ) : null}
          {selectedInput === "voice" ? (
            <div className="voice-inspector">
              <div className="voice-avatar"><AudioLines size={24} /></div>
              <div className="voice-copy">
                <p className="panel-label"><AudioLines size={14} /> AUTHORIZED REFERENCE SPEECH</p>
                <h2>Reference speech gives the target character a voice.</h2>
                <p>It supplies speaker identity and method-specific voice style, not the target line itself.</p>
              </div>
              <MiniWaveform tone="voice" />
            </div>
          ) : null}
        </section>

        <section className="global-timeline" aria-label="Synchronized timeline">
          <div className="timeline-toolbar">
            <button aria-label={isPlaying ? "Pause task timeline" : "Play task timeline"} className="timeline-play" onClick={() => setIsPlaying((playing) => !playing)} type="button">
              {isPlaying ? <Pause fill="currentColor" size={15} /> : <CirclePlay fill="currentColor" size={16} />}
            </button>
            <span className="timeline-time">{timecode}</span>
            <span className="timeline-title">ONE SYNCHRONIZED TIMELINE</span>
            <span className="timeline-status"><span /> Concept case</span>
          </div>
          <div className="tracks">
            <Track label="VIDEO" tone="video"><div className="frame-strip">{Array.from({ length: 12 }, (_, index) => <img alt="" key={index} src="/atlas/demo/scene-v1.png" style={{ objectPosition: `${35 + index * 3}% center` }} />)}</div></Track>
            <Track label="PHONEMES" tone="text"><div className="phoneme-track">{phonemes.map((phoneme) => <span key={phoneme.value} style={{ left: `${phoneme.start}%`, width: `${phoneme.width}%` }}>{phoneme.value}</span>)}</div></Track>
            <Track label="PROSODY" tone="prosody"><ProsodyLine /></Track>
            <Track label="OUTPUT" tone="output"><MiniWaveform tone="output" /></Track>
          </div>
          <input aria-label="Synchronized task time" className="timeline-range" max="100" min="0" onChange={(event) => setTimePercent(Number(event.target.value))} type="range" value={timePercent} />
          <span className="playhead" style={{ left: `calc(104px + (100% - 126px) * ${timePercent / 100})` }} />
        </section>
      </section>
    </main>
  );
}

function InputButton({ active, detail, icon, label, onClick, title }: { active: boolean; detail: string; icon: React.ReactNode; label: string; onClick: () => void; title: string }) {
  return (
    <button aria-pressed={active} aria-label={label} className={`task-input ${active ? "is-active" : ""}`} onClick={onClick} type="button">
      <span className="input-icon">{icon}</span>
      <span><strong>{title}</strong><small>{detail}</small></span>
      <ChevronRight size={15} />
    </button>
  );
}

function SpeechOutput() {
  return (
    <div className="speech-output" role="tabpanel">
      <div className="output-badge"><Waves size={14} /> TARGET SPEECH</div>
      <MiniWaveform tone="output" />
      <div className="spectrogram" aria-label="Illustrative mel spectrogram">
        {Array.from({ length: 42 }, (_, index) => <span key={index} style={{ height: `${22 + ((index * 17) % 62)}%`, opacity: 0.25 + ((index * 11) % 60) / 100 }} />)}
      </div>
      <div className="output-meta"><span>Mel-spectrogram</span><span>Waveform</span><span className="mode-pill">CONCEPT</span></div>
    </div>
  );
}

function DubbedVideoOutput() {
  return (
    <div className="dubbed-output" role="tabpanel">
      <div className="output-video-frame"><img alt="Fictional actor with target dubbing preview" src="/atlas/demo/scene-v1.png" /><span><Waves size={14} /> TARGET SPEECH MUXED</span></div>
      <p>OpenDub turns the research output into a reviewable, exportable dubbed video.</p>
    </div>
  );
}

function Track({ children, label, tone }: { children: React.ReactNode; label: string; tone: string }) {
  return <div className={`timeline-track ${tone}`}><span>{label}</span><div>{children}</div></div>;
}

function MiniWaveform({ tone }: { tone: "voice" | "output" }) {
  return <div className={`mini-waveform ${tone}`} aria-label={tone === "voice" ? "Reference speech waveform" : "Generated speech waveform"}>{waveformBars.map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}</div>;
}

function ProsodyLine() {
  return <svg aria-label="Illustrative pitch and energy trajectory" className="prosody-line" viewBox="0 0 600 42" preserveAspectRatio="none"><path d="M0 30 C30 29 44 8 72 18 S110 32 140 20 S180 4 205 16 S244 32 270 21 S320 11 345 20 S385 32 412 16 S452 6 480 19 S530 30 600 12" fill="none" pathLength="1" /></svg>;
}
