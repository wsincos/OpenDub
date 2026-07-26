import { useState } from "react";

const layers = [
  { id: "lip", label: "Lip motion", relation: "Lip -> duration", detail: "Short-range mouth motion constrains phoneme timing.", tone: "lip" },
  { id: "face", label: "Face affect", relation: "Face -> F0 + energy", detail: "Local facial affect conditions pitch and energy trajectories.", tone: "face" },
  { id: "scene", label: "Scene context", relation: "Scene -> global emotion", detail: "Scene-level context supplies a global emotional condition.", tone: "scene" },
] as const;

export function HpmHierarchyView() {
  const [activeId, setActiveId] = useState<(typeof layers)[number]["id"]>("lip");
  const active = layers.find((layer) => layer.id === activeId) ?? layers[0];

  return (
    <section className="concept-view hpm-concept" aria-label="HPMDubbing hierarchy concept view">
      <ConceptHeading eyebrow="HIERARCHICAL PROSODY / CONCEPT" title="Three visual scales, three prosody roles." />
      <div className="hpm-layout">
        <div className="hpm-layer-stack" aria-label="HPM visual hierarchy">
          {layers.map((layer, index) => (
            <button aria-pressed={active.id === layer.id} className={`hpm-layer ${layer.tone} ${active.id === layer.id ? "is-active" : ""}`} key={layer.id} onClick={() => setActiveId(layer.id)} type="button">
              <span>0{index + 1}</span><strong>{layer.label}</strong><small>{layer.relation}</small>
            </button>
          ))}
          <div className="hpm-convergence"><i /><i /><i /><span>Hierarchical prosody</span></div>
        </div>
        <div className="hpm-focus" data-tone={active.tone}>
          <p>ACTIVE RELATION</p>
          <h3>{active.label} {"->"} {active.relation.split(" -> ")[1]}</h3>
          <p>{active.detail}</p>
          <div className="hpm-signal-visual" aria-label={`Illustrative ${active.relation} signal`}>
            {Array.from({ length: 28 }, (_, index) => <i key={index} style={{ height: `${18 + ((index * (activeId.length + 5)) % 68)}%` }} />)}
          </div>
          <span className="illustrative-tag">ILLUSTRATIVE SIGNAL</span>
        </div>
      </div>
    </section>
  );
}

export function ConceptHeading({ eyebrow, title }: { eyebrow: string; title: string }) {
  return <header className="concept-heading"><p>{eyebrow}</p><h2>{title}</h2><span>CONCEPT</span></header>;
}
