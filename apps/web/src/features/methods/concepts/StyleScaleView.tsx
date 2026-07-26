import { useState } from "react";

import { ConceptHeading } from "./HpmHierarchyView";

type Scale = "frame" | "phoneme";

const phonemes = ["ni", "zhong", "yu", "lai", "le"];

export function StyleScaleView() {
  const [scale, setScale] = useState<Scale>("frame");

  return (
    <section className="concept-view style-concept" aria-label="StyleDubber scale concept view">
      <ConceptHeading eyebrow="MULTI-SCALE STYLE / CONCEPT" title="Local pronunciation, global character style." />
      <div className="style-layout">
        <div className="scale-toggle" role="group" aria-label="Style explanation scale">
          <button aria-pressed={scale === "frame"} className={scale === "frame" ? "is-active" : ""} onClick={() => setScale("frame")} type="button">Frame scale</button>
          <button aria-pressed={scale === "phoneme"} className={scale === "phoneme" ? "is-active" : ""} onClick={() => setScale("phoneme")} type="button">Phoneme scale</button>
        </div>
        {scale === "frame" ? <FrameGroups /> : <PhonemeGroups />}
        <div className="utterance-band"><span>USL</span><div><i /><i /><i /><i /><i /></div><strong>Utterance-level style condition</strong></div>
      </div>
    </section>
  );
}

function FrameGroups() {
  return <div className="frame-groups" aria-label="Frame groups"><p>Frame groups</p><div>{Array.from({ length: 18 }, (_, index) => <i key={index}><span>{index % 3 === 0 ? "lip" : "frame"}</span></i>)}</div><small>Several visual frames inform one stable phoneme-level style unit.</small></div>;
}

function PhonemeGroups() {
  return <div className="phoneme-groups" aria-label="Grouped phoneme intervals"><p>Grouped phoneme intervals</p><div>{phonemes.map((phoneme, index) => <span key={phoneme} style={{ flex: index === 1 || index === 3 ? 1.55 : 1 }}>{phoneme}</span>)}</div><small>MPA and PLA operate on aligned phoneme intervals before global style learning.</small></div>;
}
