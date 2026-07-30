import { BookOpen, ExternalLink, Film, Pause, Play, Radio, ScanSearch, ShieldCheck, Waves } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

import { getMethodById } from "../../content/methods";
import { getShowcaseCase, publicShowcaseUrl, type ShowcaseArtifact, type ShowcaseCase } from "../../content/showcases";
import { ArchiveWaveform } from "../showcases/ArchiveWaveform";
import { useSynchronizedArchivePlayback } from "../showcases/useSynchronizedArchivePlayback";
import { ArchiveAcousticView } from "./ArchiveAcousticView";
import "./comparison-lab.css";

const ARCHIVE_CASE_ORDER = ["case-03", "case-04", "animation-1", "human-0"] as const;
const ARCHIVE_CASES = ARCHIVE_CASE_ORDER.map(getShowcaseCase).filter((item): item is ShowcaseCase => Boolean(item));
const SCENE_LABELS: Record<string, string> = {
  "case-03": "Animated cinematic scene",
  "case-04": "Presenter and display scene",
  "animation-1": "Animated character scene",
  "human-0": "Human portrait scene",
};

const METHOD_CONTEXT: Record<NonNullable<ShowcaseArtifact["methodId"]>, { accent: string; focus: string; detail: string }> = {
  "galaxycong/hpmdubbing": {
    accent: "#66bde7",
    focus: "VISUAL PROSODY ACROSS LIP, FACE, AND SCENE",
    detail: "Visual prosody is distributed across lip timing, facial affect, and scene atmosphere.",
  },
  "galaxycong/styledubber": {
    accent: "#b6a2ed",
    focus: "LOCAL PRONUNCIATION, GLOBAL CHARACTER STYLE",
    detail: "Phoneme-scale pronunciation is read with utterance-level character style.",
  },
  "galaxycong/emodubber": {
    accent: "#ef8d9d",
    focus: "ALIGNMENT, IDENTITY, AND DIRECTED EMOTION",
    detail: "The complete method joins audiovisual alignment, pronunciation, identity, and user-directed emotion.",
  },
};

const REFERENCE_CONTEXT = { accent: "#83d6c0", focus: "REFERENCE PERFORMANCE", detail: "The archived synchronized scene speech used as a listening reference." };

function trackId(caseItem: ShowcaseCase, artifact: ShowcaseArtifact) {
  return `${caseItem.id}:${artifact.path}`;
}

function formatTime(value: number) {
  return `00:${value.toFixed(3).padStart(6, "0")}`;
}

function caseNumber(caseItem: ShowcaseCase) {
  const index = ARCHIVE_CASES.findIndex((item) => item.id === caseItem.id);
  return String(index + 1).padStart(2, "0");
}

function sceneLabel(caseItem: ShowcaseCase) {
  return SCENE_LABELS[caseItem.id] ?? caseItem.displayName;
}

export function ComparisonLabPage() {
  const [activeCaseId, setActiveCaseId] = useState(ARCHIVE_CASES[0]?.id ?? "");
  const activeCase = ARCHIVE_CASES.find((caseItem) => caseItem.id === activeCaseId) ?? ARCHIVE_CASES[0];
  const [activePath, setActivePath] = useState(activeCase?.artifacts[0]?.path ?? "");
  const stageHeading = useRef<HTMLHeadingElement>(null);
  const playback = useSynchronizedArchivePlayback();

  if (!activeCase) throw new Error("Compare requires at least one admitted archive case.");

  const activeArtifact = activeCase.artifacts.find((artifact) => artifact.path === activePath) ?? activeCase.artifacts[0];
  if (!activeArtifact) throw new Error(`Archive ${activeCase.id} requires at least one artifact.`);
  const activeMethod = activeArtifact.methodId ? getMethodById(activeArtifact.methodId) : undefined;
  const activeSceneLabel = sceneLabel(activeCase);

  useEffect(() => {
    playback.selectTrack(trackId(activeCase, activeArtifact));
  }, [activeArtifact, activeCase, playback.selectTrack]);

  function selectCase(caseItem: ShowcaseCase) {
    if (caseItem.id === activeCase.id) return;
    playback.reset();
    setActiveCaseId(caseItem.id);
    setActivePath(caseItem.artifacts[0]?.path ?? "");
    window.setTimeout(() => stageHeading.current?.focus(), 0);
  }

  function selectSource(path: string) {
    if (path === activeArtifact.path) return;
    if (playback.status === "ended") playback.seek(0);
    setActivePath(path);
  }

  return (
    <main className="compare-listening-desk">
      <header className="compare-listening-intro">
        <p><Radio size={13} /> ARCHIVED LISTENING DESK</p>
        <h1>One archive, several original method readings.</h1>
        <div className="compare-listening-intro-bottom">
          <span>OpenDub gathers historical team-provided scenes for direct inspection: one selected video/audio record, its real file-derived acoustic views, and the original complete methods behind each archived output.</span>
          <a href="#archive-record">ARCHIVE RECORD <ScanSearch size={13} /></a>
        </div>
      </header>

      <section aria-label="Archive scene index" className="compare-scene-index">
        <div className="compare-section-heading"><span>SCENE INDEX</span><small>{ARCHIVE_CASES.length.toString().padStart(2, "0")} ARCHIVED CONTEXTS</small></div>
        <div className="compare-scene-grid">
          {ARCHIVE_CASES.map((caseItem) => {
            const selected = caseItem.id === activeCase.id;
            return (
              <button
                aria-pressed={selected}
                aria-label={`Select Case ${caseNumber(caseItem)}: ${sceneLabel(caseItem)}`}
                className={selected ? "compare-scene-tile is-active" : "compare-scene-tile"}
                key={caseItem.id}
                onClick={() => selectCase(caseItem)}
                type="button"
              >
                <img alt="" src={caseItem.posterUrl} />
                <span>CASE {caseNumber(caseItem)}</span>
                <strong>{sceneLabel(caseItem)}</strong>
                <small>{formatTime(caseItem.durationSeconds)} · ARCHIVED</small>
              </button>
            );
          })}
        </div>
      </section>

      <section aria-label={`${activeSceneLabel} archived listening`} className="compare-listening-stage">
        <div className="compare-stage-meta">
          <span>ARCHIVED SAME-SCENE LISTENING</span>
          <strong>{formatTime(playback.currentTime)} / {formatTime(activeCase.durationSeconds)}</strong>
          <small>No automatic ranking. This archive does not yet establish a verified common-input benchmark.</small>
        </div>
        <div aria-label={`Case ${caseNumber(activeCase)}, active source: ${activeArtifact.label}`} className="compare-video-frame">
          {activeCase.artifacts.map((artifact) => {
            const isActive = artifact.path === activeArtifact.path;
            return (
              <video
                aria-label={`Case ${caseNumber(activeCase)}, ${artifact.label} source`}
                className={isActive ? "is-active" : ""}
                key={`${activeCase.id}:${artifact.path}`}
                loop={false}
                muted={!isActive}
                onEnded={() => playback.handleEnded(trackId(activeCase, artifact))}
                onTimeUpdate={(event) => playback.updateCurrentTime(trackId(activeCase, artifact), event.currentTarget.currentTime)}
                playsInline
                poster={activeCase.posterUrl}
                preload="metadata"
                ref={(player) => playback.registerTrack(trackId(activeCase, artifact), player)}
                src={publicShowcaseUrl(activeCase, artifact.path)}
              />
            );
          })}
          <span className="compare-video-corner"><Film size={13} /> SELECTED SOURCE / MATCHED AUDIO</span>
        </div>
        <div className="compare-timeline-control">
          <button
            aria-label={playback.status === "playing" ? "Pause active source" : "Play active source"}
            onClick={() => playback.status === "playing" ? playback.pauseActive() : void playback.playActive()}
            title={playback.status === "playing" ? "Pause active source" : "Play active source"}
            type="button"
          >{playback.status === "playing" ? <Pause size={16} /> : <Play size={16} />}</button>
          <input aria-label="Shared visual timebase" max={activeCase.durationSeconds} min="0" onChange={(event) => playback.seek(Number(event.currentTarget.value))} step="0.001" type="range" value={playback.currentTime} />
          <span aria-live="polite">{playback.status === "playing" ? `PLAYING · ${activeArtifact.label}` : `READY TO PLAY · ${activeArtifact.label}`}</span>
        </div>
      </section>

      <section aria-label={`${activeSceneLabel} source channels`} className="compare-source-rails">
        <div className="compare-section-heading"><span>SOURCE CHANNELS</span><small>ONE SELECTED OUTPUT IS AUDIBLE</small></div>
        <div className="compare-source-grid">
          {activeCase.artifacts.map((artifact) => {
            const context = artifact.methodId ? METHOD_CONTEXT[artifact.methodId] : REFERENCE_CONTEXT;
            const isActive = artifact.path === activeArtifact.path;
            return (
              <button
                aria-current={isActive ? "true" : undefined}
                aria-label={`Select ${artifact.label} source`}
                className={isActive ? "compare-source-rail is-active" : "compare-source-rail"}
                key={artifact.path}
                onClick={() => selectSource(artifact.path)}
                style={{ "--source-color": context.accent } as React.CSSProperties}
                type="button"
              >
                <span>{artifact.role === "ground_truth" ? "REFERENCE PERFORMANCE" : "ARCHIVED METHOD OUTPUT"}</span>
                <strong>{artifact.label}</strong>
                <ArchiveWaveform color={context.accent} featureUrl={artifact.featureUrl} label={`Case ${caseNumber(activeCase)} ${artifact.label}`} />
              </button>
            );
          })}
        </div>
      </section>

      <ArchiveAcousticView activeArtifact={activeArtifact} activeCase={activeCase} currentTime={playback.currentTime} onSeek={playback.seek} />

      <section aria-label="Archive contract limitations" className="compare-archive-boundary">
        <div><span>CANONICAL TRANSCRIPT · NOT ATTACHED TO THIS ARCHIVE</span><small>Do not infer dialogue from the video.</small></div>
        <div><span>REFERENCE-SPEECH CONTRACT · NOT PUBLISHED WITH THIS ARCHIVE</span><small>Listening is available; benchmark comparison is not.</small></div>
      </section>

      <section aria-label="Original method readings" className="compare-method-differences">
        <div className="compare-method-heading"><div><p>READ THE ORIGINAL METHODS</p><h2>Complete methods illuminate different video-dubbing conditions.</h2></div><Waves size={19} /></div>
        <div className="compare-method-rows">
          {activeCase.artifacts.filter((artifact) => artifact.methodId).map((artifact) => {
            const context = METHOD_CONTEXT[artifact.methodId!];
            const method = getMethodById(artifact.methodId);
            return (
              <article key={artifact.path} style={{ "--source-color": context.accent } as React.CSSProperties}>
                <span>TEAM-DEVELOPED COMPLETE METHOD</span>
                <h3>{artifact.label}</h3>
                <strong>{context.focus}</strong>
                <p>{context.detail}</p>
                {method ? <Link to={`/methods/${method.slug}`}>INSPECT ORIGINAL METHOD <ExternalLink size={13} /></Link> : null}
              </article>
            );
          })}
        </div>
      </section>

      <section className="compare-archive-record" id="archive-record">
        <div><p>ARCHIVE RECORD</p><h2 ref={stageHeading} tabIndex={-1}>Bounded evidence, retained provenance.</h2></div>
        <dl>
          <div><dt>STATUS</dt><dd>Historical team-provided result. Not a fresh OpenDub run.</dd></div>
          <div><dt>CASE</dt><dd>CASE {caseNumber(activeCase)} · {activeCase.id} · {activeSceneLabel} · {formatTime(activeCase.durationSeconds)}</dd></div>
          <div><dt>ACTIVE SOURCE HASH</dt><dd>{activeArtifact.sha256}</dd></div>
          <div><dt>PUBLISHED RECORD</dt><dd>{activeMethod ? <a href={activeMethod.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={13} /> PUBLISHED RECORD</a> : "Select a method output to inspect its published record."}</dd></div>
          <div><dt>EVIDENCE BOUNDARY</dt><dd><ShieldCheck size={13} /> Archived same-scene listening only. No automated ranking, metric, Replay, or Live claim.</dd></div>
        </dl>
      </section>
    </main>
  );
}
