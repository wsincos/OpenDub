import { ExternalLink, Film, Play, ShieldCheck, Volume2 } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { getMethodById } from "../../content/methods";
import { publicShowcaseUrl, showcaseCases, type ShowcaseArtifact, type ShowcaseCase } from "../../content/showcases";
import { ArchiveWaveform } from "./ArchiveWaveform";
import "./example-gallery.css";
import { type ShowcasePlayback, useExclusiveShowcasePlayback } from "./useExclusiveShowcasePlayback";

type ExampleGalleryPageProps = { embedded?: boolean };

const GALLERY_CASES = showcaseCases.filter((showcase) => showcase.mediaRelease === "v2");

export function ExampleGalleryPage({ embedded = false }: ExampleGalleryPageProps) {
  const [activeCaseId, setActiveCaseId] = useState(GALLERY_CASES[0]?.id ?? "");
  const { activePlayback, handlePause, handlePlay, registerPlayer, resetAll } = useExclusiveShowcasePlayback();
  const activeCase = GALLERY_CASES.find((showcase) => showcase.id === activeCaseId) ?? GALLERY_CASES[0];

  if (!activeCase) throw new Error("The V2 archive gallery requires at least one admitted case.");

  function selectCase(caseId: string) {
    resetAll();
    setActiveCaseId(caseId);
  }

  const content = (
    <>
      <header className="gallery-heading">
        <div>
          <p className="vtts-kicker"><Film size={13} /> ARCHIVED METHOD EXAMPLES</p>
          <h1>Inspect the work, not a promise.</h1>
          <p>Two provided case families retain their method identity, historical status, and media provenance. They are not presented as a new OpenDub run or a fair same-input benchmark.</p>
        </div>
        <Link className="gallery-evidence-link" to="/evidence"><ShieldCheck size={15} /> Evidence boundary <ExternalLink size={13} /></Link>
      </header>

      <div aria-label="Showcase case family" className="gallery-tabs" role="tablist">
        {GALLERY_CASES.map((showcase, index) => (
          <button aria-selected={activeCase.id === showcase.id} key={showcase.id} onClick={() => selectCase(showcase.id)} role="tab" type="button">
            <span>{String(index + 1).padStart(2, "0")}</span>{showcase.visualType === "human" ? "Human portrait" : "Animated character"}
          </button>
        ))}
      </div>

      <div aria-label={`${activeCase.displayName} media panels`} className="example-media-grid" role="tabpanel">
        {activeCase.artifacts.map((artifact) => (
          <ExampleMediaPanel
            activePlayback={activePlayback}
            artifact={artifact}
            caseItem={activeCase}
            key={artifact.path}
            onPause={handlePause}
            onPlay={handlePlay}
            registerPlayer={registerPlayer}
          />
        ))}
      </div>

      <footer className="gallery-boundary">
        <span><ShieldCheck size={14} /> Archived research example. Not a fresh OpenDub run.</span>
        <span>Case contract: {activeCase.id} · historical output · comparison remains evidence-gated</span>
      </footer>
    </>
  );

  return embedded
    ? <section className="example-gallery example-gallery-embedded" id="examples">{content}</section>
    : <main className="example-gallery example-gallery-page">{content}</main>;
}

type ExampleMediaPanelProps = {
  activePlayback: ShowcasePlayback | null;
  artifact: ShowcaseArtifact;
  caseItem: ShowcaseCase;
  onPause: (caseId: string, artifactPath: string) => void;
  onPlay: (caseId: string, artifactPath: string, player: HTMLVideoElement) => void;
  registerPlayer: (caseId: string, artifactPath: string, player: HTMLVideoElement | null) => void;
};

function ExampleMediaPanel({ activePlayback, artifact, caseItem, onPause, onPlay, registerPlayer }: ExampleMediaPanelProps) {
  const method = artifact.methodId ? getMethodById(artifact.methodId) : undefined;
  const isActive = activePlayback?.caseId === caseItem.id && activePlayback.artifactPath === artifact.path;
  const isPlaying = isActive && activePlayback.isPlaying;
  const roleLabel = artifact.role === "ground_truth" ? "REFERENCE PERFORMANCE" : "TEAM-DEVELOPED METHOD OUTPUT";

  return (
    <article className={isActive ? "example-media-panel is-active-artifact" : "example-media-panel"}>
      <div className="example-media-title">
        <span className={artifact.role === "ground_truth" ? "media-role is-ground-truth" : "media-role"}>{artifact.role === "ground_truth" ? "REF" : "METHOD"}</span>
        <div><span>{roleLabel}</span><h2>{artifact.label}</h2></div>
        {method ? <Link aria-label={`Inspect ${artifact.label} method`} to={`/methods/${method.slug}`}><ExternalLink size={14} /></Link> : null}
      </div>
      <div className="example-video-shell">
        <video
          aria-label={`${caseItem.displayName}, ${artifact.label}`}
          controls
          onEnded={() => onPause(caseItem.id, artifact.path)}
          onPause={() => onPause(caseItem.id, artifact.path)}
          onPlay={(event) => onPlay(caseItem.id, artifact.path, event.currentTarget)}
          playsInline
          poster={caseItem.posterUrl}
          preload="metadata"
          ref={(player) => registerPlayer(caseItem.id, artifact.path, player)}
          src={publicShowcaseUrl(caseItem, artifact.path)}
        />
        <span aria-live="polite" className="example-video-status">
          {isPlaying ? <><Volume2 size={11} /> AUDIBLE: {artifact.label}</> : <><Play size={11} /> READY · AUDIO IDLE</>}
        </span>
      </div>
      <div className="example-media-meta">
        <span>{caseItem.contentStatus === "replay" ? "Verified Replay" : "Archived research example"}</span>
        <span>{caseItem.durationSeconds.toFixed(3)} s · paired source video and audio</span>
        <ArchiveWaveform color={artifact.role === "ground_truth" ? "#83d6c0" : "#7fbad2"} featureUrl={artifact.featureUrl} label={`${artifact.label} archive`} />
      </div>
    </article>
  );
}
