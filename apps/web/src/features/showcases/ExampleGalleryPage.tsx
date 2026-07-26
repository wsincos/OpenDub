import { ExternalLink, Film, Pause, Play, ShieldCheck } from "lucide-react";
import { useRef, useState } from "react";
import { Link } from "react-router-dom";

import { publicShowcaseUrl, showcaseCases, type ShowcaseArtifact, type ShowcaseCase } from "../../content/showcases";
import "./example-gallery.css";

type ExampleGalleryPageProps = { embedded?: boolean };

export function ExampleGalleryPage({ embedded = false }: ExampleGalleryPageProps) {
  const [activeCaseId, setActiveCaseId] = useState(showcaseCases[0].id);
  const players = useRef<HTMLVideoElement[]>([]);
  const activeCase = showcaseCases.find((showcase) => showcase.id === activeCaseId) ?? showcaseCases[0];

  function pauseOtherPlayers(current: HTMLVideoElement) {
    players.current.forEach((player) => {
      if (player !== current) player.pause();
    });
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
          <button aria-selected={activeCase.id === showcase.id} key={showcase.id} onClick={() => setActiveCaseId(showcase.id)} role="tab" type="button">
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
            onPlay={pauseOtherPlayers}
            registerPlayer={(player) => {
              if (player && !players.current.includes(player)) players.current.push(player);
            }}
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
  artifact: ShowcaseArtifact;
  caseItem: ShowcaseCase;
  onPlay: (player: HTMLVideoElement) => void;
  registerPlayer: (player: HTMLVideoElement | null) => void;
};

function ExampleMediaPanel({ artifact, caseItem, onPlay, registerPlayer }: ExampleMediaPanelProps) {
  const [playing, setPlaying] = useState(false);
  const methodSlug = artifact.methodId?.split("/")[1];
  const source = publicShowcaseUrl(caseItem.id, artifact.path);
  const label = `${caseItem.displayName}, ${artifact.label}`;

  return (
    <article className="example-media-panel">
      <div className="example-media-title">
        <span className={artifact.role === "ground_truth" ? "media-role is-ground-truth" : "media-role"}>{artifact.role === "ground_truth" ? "GT" : "METHOD"}</span>
        <h3>{artifact.label}</h3>
        {methodSlug ? <Link aria-label={`Inspect ${artifact.label} method`} to={`/methods/${methodSlug}`}><ExternalLink size={14} /></Link> : null}
      </div>
      <div className="example-video-shell">
        <video aria-label={label} controls onPause={() => setPlaying(false)} onPlay={(event) => { onPlay(event.currentTarget); setPlaying(true); }} playsInline poster={caseItem.posterUrl} preload="metadata" ref={registerPlayer} src={source} />
        <span className="example-video-status">{playing ? <><Pause size={11} /> PLAYING</> : <><Play size={11} /> READY</>}</span>
      </div>
      <div className="example-media-meta"><span>{caseItem.contentStatus === "replay" ? "Verified Replay" : "Archived research example"}</span><span>Audio and video paired</span></div>
    </article>
  );
}
