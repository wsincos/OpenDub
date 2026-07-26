import { ArrowUpRight, ChevronRight, FolderPlus, GitBranch, ScanSearch } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { englishIndefiniteArticle, getMethodById, MethodDefinition, methods } from "../../content/methods";
import "./method-atlas.css";

type DecisionNeed = {
  id: "prosody" | "style" | "emotion";
  label: string;
  zhLabel: string;
  methodId: MethodDefinition["id"];
  orientation: string;
};

const decisionNeeds: DecisionNeed[] = [
  {
    id: "prosody",
    label: "Visual prosody and scene rhythm",
    zhLabel: "视觉韵律与场景节奏",
    methodId: "galaxycong/hpmdubbing",
    orientation: "Prioritize the hierarchy of lip motion, facial affect, and scene context when inspecting or preparing a complete method.",
  },
  {
    id: "style",
    label: "Pronunciation and character style",
    zhLabel: "发音清晰度与角色风格",
    methodId: "galaxycong/styledubber",
    orientation: "Prioritize local phoneme alignment and utterance-level character style when inspecting or preparing a complete method.",
  },
  {
    id: "emotion",
    label: "Explicit emotion direction",
    zhLabel: "显式情感方向",
    methodId: "galaxycong/emodubber",
    orientation: "Prioritize the paper's explicit emotion category and intensity conditions when inspecting or preparing a complete method.",
  },
];

export function MethodAtlasPage() {
  const [selectedNeedId, setSelectedNeedId] = useState<DecisionNeed["id"]>("prosody");
  const selectedNeed = decisionNeeds.find((need) => need.id === selectedNeedId) ?? decisionNeeds[0];
  const selectedMethod = getMethodById(selectedNeed.methodId);

  return (
    <main className="method-atlas">
      <section className="atlas-header">
        <div><p className="atlas-eyebrow">RESEARCH PROGRESSION / 研究路径</p><h1>Three complete paths through the same video dubbing task.</h1></div>
        <p>OpenDub keeps each research method intact, then makes its inputs, components, signals, and evidence explorable. 保留完整方法，而不是拼接内部模块。</p>
      </section>
      {selectedMethod ? <MethodDecisionGuide method={selectedMethod} onSelect={setSelectedNeedId} selectedNeed={selectedNeed} /> : null}
      <section className="method-progression" aria-label="Video dubbing method progression">
        <div className="progression-line" />
        {methods.map((method, index) => (
          <article className="method-entry" key={method.id} style={{ "--method-color": method.color } as React.CSSProperties}>
            <div className="year-marker"><span>{method.year}</span><i>{index + 1}</i></div>
            <div className="method-summary">
              <p>{method.venue.toUpperCase()} · {method.status}</p>
              <h2>{method.title}</h2>
              <h3>{method.question}</h3>
              <span>{method.contribution}</span>
            </div>
            <div className="method-mini-flow" aria-label={`${method.title} method flow`}>
              {method.overviewNodeIds.slice(0, 4).map((nodeId, nodeIndex) => {
                const node = method.nodes.find((item) => item.id === nodeId);
                return node ? <div key={node.id}><b>{node.short}</b>{nodeIndex < 3 ? <ChevronRight size={15} /> : null}</div> : null;
              })}
            </div>
            <div className="method-actions">
              <Link aria-label={`Explore method ${method.title}`} to={`/methods/${method.slug}`}><ScanSearch size={15} /> Explore method</Link>
              <Link aria-label={`Prepare ${englishIndefiniteArticle(method.title)} ${method.title} project`} className="prepare-project" to={`/studio?method=${method.slug}`}><FolderPlus size={14} /> Prepare project</Link>
              <a href={method.paperUrl} rel="noreferrer" target="_blank">Paper <ArrowUpRight size={13} /></a>
              <a href={method.sourceUrl} rel="noreferrer" target="_blank">Source <GitBranch size={13} /></a>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}

function MethodDecisionGuide({ method, onSelect, selectedNeed }: { method: MethodDefinition; onSelect: (id: DecisionNeed["id"]) => void; selectedNeed: DecisionNeed }) {
  return (
    <section className="decision-guide" aria-label="Choose a complete method by primary need">
      <div className="decision-heading"><p>CHOOSE BY PRIMARY NEED / 按首要需求选择</p><h2>Choose what you need to inspect and prepare first.</h2></div>
      <div className="decision-options" role="group" aria-label="Primary video dubbing need">
        {decisionNeeds.map((need) => <button aria-pressed={selectedNeed.id === need.id} className={selectedNeed.id === need.id ? "is-active" : ""} key={need.id} onClick={() => onSelect(need.id)} type="button"><strong>{need.label}</strong><span>{need.zhLabel}</span></button>)}
      </div>
      <div className="decision-result" style={{ "--method-color": method.color } as React.CSSProperties}>
        <div><p>Recommended for inspection and preparation / 可解释导览</p><h2>{method.title}</h2><span>{selectedNeed.orientation}</span></div>
        <div className="decision-actions"><Link to={`/methods/${method.slug}`}><ScanSearch size={15} /> Inspect method and evidence</Link><Link aria-label={`Prepare ${englishIndefiniteArticle(method.title)} ${method.title} project from this recommendation`} to={`/studio?method=${method.slug}`}><FolderPlus size={15} /> Prepare this complete method</Link></div>
      </div>
      <p className="decision-boundary">This is a transparent orientation, not a claim of live runtime or global superiority. 这是选择导览，不是实时运行或全局最优结论。</p>
    </section>
  );
}
