import { ArrowUpRight, AudioLines, BookOpen, ChevronRight, Code2, Film, Layers3, Subtitles, Volume2 } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

import { methods, type MethodDefinition } from "../../content/methods";
import { PaperArchitectureFigure } from "./PaperArchitectureFigure";
import "./method-atlas.css";

const expandingMethods = ["InstructDubber", "Speaker2Dub", "..."];

export function MethodAtlasPage() {
  const [selectedMethodId, setSelectedMethodId] = useState<MethodDefinition["id"]>(methods[0].id);
  const selectedMethod = methods.find((method) => method.id === selectedMethodId) ?? methods[0];
  const emphasizedComponents = selectedMethod.overviewNodeIds
    .map((nodeId) => selectedMethod.nodes.find((node) => node.id === nodeId)?.short)
    .filter((value): value is string => Boolean(value))
    .slice(0, 4);

  return (
    <main className="method-atlas">
      <header className="atlas-header">
        <div>
          <p className="atlas-eyebrow"><Layers3 size={13} /> ORIGINAL OPENDUB METHOD FAMILY</p>
          <h1>Multiple original methods. One shared dubbing task.</h1>
        </div>
        <p>OpenDub makes our team&apos;s complete video dubbing methods readable through their source architectures, declared components, and traceable records. It does not recombine internal blocks into a new model.</p>
      </header>

      <section aria-label="Shared video dubbing task contract" className="atlas-task-contract">
        <div><Film size={15} /><span>SILENT VIDEO</span></div>
        <ChevronRight aria-hidden="true" size={16} />
        <div><Subtitles size={15} /><span>TEXT</span></div>
        <ChevronRight aria-hidden="true" size={16} />
        <div><AudioLines size={15} /><span>REFERENCE SPEECH</span></div>
        <ChevronRight aria-hidden="true" size={16} />
        <div><Volume2 size={15} /><span>TARGET SPEECH</span></div>
      </section>

      <section aria-label="Original video dubbing methods" className="atlas-method-rail">
        {methods.map((method, index) => (
          <button
            aria-label={`Inspect ${method.title} original method`}
            aria-pressed={selectedMethod.id === method.id}
            className={selectedMethod.id === method.id ? "atlas-method-card is-selected" : "atlas-method-card"}
            key={method.id}
            onClick={() => setSelectedMethodId(method.id)}
            style={{ "--method-color": method.color } as React.CSSProperties}
            type="button"
          >
            <span>0{index + 1}</span>
            <p>{method.teamLabel}</p>
            <strong>{method.title}</strong>
            <small>{method.originalFocus}</small>
          </button>
        ))}
        <aside aria-label="Expanding methods in OpenDub" className="atlas-expanding-methods">
          <p>EXPANDING METHODS</p>
          <div>{expandingMethods.map((method) => <span key={method}>{method}</span>)}</div>
          <small>In development in OpenDub.</small>
        </aside>
      </section>

      <section className="atlas-evidence-section" style={{ "--method-color": selectedMethod.color } as React.CSSProperties}>
        <div className="atlas-evidence-heading">
          <div><p>ORIGINAL METHOD EVIDENCE</p><h2>{selectedMethod.title}</h2></div>
          <span>SELECT A MARKED REGION TO READ THE ORIGINAL METHOD FIGURE</span>
        </div>
        <PaperArchitectureFigure key={selectedMethod.id} method={selectedMethod} />
        <div className="atlas-method-record">
          <div><span>RESEARCH QUESTION</span><strong>{selectedMethod.question}</strong></div>
          <div><span>DECLARED CONTRIBUTION</span><strong>{selectedMethod.contribution}</strong></div>
          <div><span>ARCHITECTURE EMPHASIS</span><strong>{emphasizedComponents.join(" · ")}</strong></div>
          <div className="atlas-method-actions">
            <a aria-label={`Open published record for ${selectedMethod.title}`} href={selectedMethod.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={14} /> PUBLISHED RECORD <ArrowUpRight size={13} /></a>
            <a href={selectedMethod.sourceUrl} rel="noreferrer" target="_blank"><Code2 size={14} /> SOURCE REVISION <ArrowUpRight size={13} /></a>
            <Link to={`/methods/${selectedMethod.slug}`}>Open interactive map <ChevronRight size={14} /></Link>
          </div>
        </div>
      </section>
    </main>
  );
}
