import { useState } from "react";

import { ConceptHeading } from "./HpmHierarchyView";

const directions = ["Warm", "Tense", "Melancholic"] as const;

export function EmoGuidanceView() {
  const [direction, setDirection] = useState<(typeof directions)[number]>("Warm");
  const [intensity, setIntensity] = useState(62);

  return (
    <section className="concept-view emo-concept" aria-label="EmoDubber conceptual flow guidance view">
      <ConceptHeading eyebrow="CONCEPTUAL FLOW VIEW" title="Guide a direction. Do not fabricate an output." />
      <div className="emo-layout">
        <div className="emo-controls">
          <p>EMOTION DIRECTION</p>
          <div className="direction-options">{directions.map((item) => <button aria-pressed={direction === item} className={direction === item ? "is-active" : ""} key={item} onClick={() => setDirection(item)} type="button">{item}</button>)}</div>
          <label htmlFor="concept-intensity">Concept emotion intensity <strong>{intensity}% guidance intensity</strong></label>
          <input aria-label="Concept emotion intensity" id="concept-intensity" max="100" min="0" onChange={(event) => setIntensity(Number(event.target.value))} type="range" value={intensity} />
          <p className="emo-boundary">No new audio generated in Concept mode.</p>
        </div>
        <div className="flow-visual" aria-label={`${direction} conceptual guidance at ${intensity} percent`}>
          <div className="flow-caption"><span>ACOUSTIC PRIOR</span><span>{direction.toUpperCase()} TARGET</span></div>
          <svg viewBox="0 0 520 172" preserveAspectRatio="none" aria-hidden="true">
            <path className="flow-base" d="M10 137 C76 134 95 42 164 73 S255 150 316 80 S410 26 510 45" />
            <path className="flow-target" d="M10 137 C76 134 95 42 164 73 S255 150 316 80 S410 26 510 45" pathLength="1" style={{ strokeDasharray: "1", strokeDashoffset: `${1 - intensity / 100}` }} />
            <path className="flow-negative" d="M48 154 C133 130 190 154 265 128 S410 116 490 144" />
            <circle cx="164" cy="73" r="6" /><circle cx="316" cy="80" r="6" /><circle cx="510" cy="45" r="7" />
          </svg>
          <div className="flow-legend"><span><i /> Positive target guidance</span><span><i /> Negative suppression direction</span></div>
        </div>
      </div>
    </section>
  );
}
