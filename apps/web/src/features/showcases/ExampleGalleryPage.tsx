import { ExternalLink, Film, Play, ShieldCheck, Volume2 } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { publicShowcaseUrl, showcaseCases, type ShowcaseArtifact, type ShowcaseCase } from "../../content/showcases";
import "./example-gallery.css";
import { type ShowcasePlayback, useExclusiveShowcasePlayback } from "./useExclusiveShowcasePlayback";

type ExampleGalleryPageProps = { embedded?: boolean };

export function ExampleGalleryPage({ embedded = false }: ExampleGalleryPageProps) {
  const [activeCaseId, setActiveCaseId] = useState(showcaseCases[0].id);
  const { activePlayback, handlePause, handlePlay, registerPlayer, resetAll } = useExclusiveShowcasePlayback();
  const activeCase = showcaseCases.find((showcase) => showcase.id === activeCaseId) ?? showcaseCases[0];

  function selectCase(caseId: string) {
    resetAll();
    setActiveCaseId(caseId);
  }

  const content = (
    <>
      <header className="gallery-heading">
        <div>
          <p className="vtts-kicker"><Film size={13} /> ARCHIVED METHOD EXAMPLES</p>
          <h2>Inspect the work, not a promise.</h2>
          <p>Two provided case families retain their method identity, historical status, and media provenance. They are not presented as a new OpenDub run or a fair same-input benchmark.</p>
        </div>
        <Link className="gallery-evidence-link" to="/evidence"><ShieldCheck size={15} /> Evidence boundary <ExternalLink size={13} /></Link>
      </header>
      <div aria-label="Showcase case family" className="gallery-tabs" role="tablist">
        {showcaseCases.map((showcase) => (
          <button aria-selected={activeCase.id === showcase.id} key={showcase.id} onClick={() => selectCase(showcase.id)} role="tab" type="button">
            <span>{showcase.visualType === "human" ? "01" : "02"}</span>{showcase.visualType === "human" ? "Human portrait" : "Animated character"}
          </button>
        ))}
      </div>
      <div aria-label={`${activeCase.displayName} media panels`} className="example-media-grid" role="tabpanel">
        {activeCase.artifacts.map((artifact) => (
          <ExampleMediaPanel
            artifact={artifact}
            caseItem={activeCase}
            key={artifact.path}
            activePlayback={activePlayback}
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

  return embedded ? <section className="example-gallery example-gallery-embedded" id="examples">{content}</section> : <main className="example-gallery example-gallery-page">{content}</main>;
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
  const methodSlug = artifact.methodId?.split("/")[1];
  const source = publicShowcaseUrl(caseItem.id, artifact.path);
  const label = `${caseItem.displayName}, ${artifact.label}`;
  const isActive = activePlayback?.caseId === caseItem.id && activePlayback.artifactPath === artifact.path;
  const isPlaying = isActive && activePlayback.isPlaying;

  return (
    <article className={isActive ? "example-media-panel is-active-artifact" : "example-media-panel"}>
      <div className="example-media-title">
        <span className={artifact.role === "ground_truth" ? "media-role is-ground-truth" : "media-role"}>{artifact.role === "ground_truth" ? "GT" : "METHOD"}</span>
        <h3>{artifact.label}</h3>
        {methodSlug ? <Link aria-label={`Inspect ${artifact.label} method`} to={`/methods/${methodSlug}`}><ExternalLink size={14} /></Link> : null}
      </div>
      <div className="example-video-shell">
        <video aria-label={label} controls onEnded={() => onPause(caseItem.id, artifact.path)} onPause={() => onPause(caseItem.id, artifact.path)} onPlay={(event) => onPlay(caseItem.id, artifact.path, event.currentTarget)} playsInline poster={caseItem.posterUrl} preload="metadata" ref={(player) => registerPlayer(caseItem.id, artifact.path, player)} src={source} />
        <span aria-live="polite" className="example-video-status">{isPlaying ? <><Volume2 size={11} /> AUDIBLE: {artifact.label}</> : <><Play size={11} /> READY · AUDIO IDLE</>}</span>
      </div>
      <div className="example-media-meta"><span>{caseItem.contentStatus === "replay" ? "Verified Replay" : "Archived research example"}</span><span>Audio and video paired</span></div>
    </article>
  );
}
