import { ArrowUpRight, ChevronRight, GitBranch, ScanSearch } from "lucide-react";
import { Link } from "react-router-dom";

import { methods } from "../../content/methods";
import "./method-atlas.css";

export function MethodAtlasPage() {
  return (
    <main className="method-atlas">
      <section className="atlas-header">
        <div><p className="atlas-eyebrow">RESEARCH PROGRESSION</p><h1>Three complete paths through the same video dubbing task.</h1></div>
        <p>OpenDub keeps each research method intact, then makes its inputs, components, signals, and evidence explorable.</p>
      </section>
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
              <a href={method.paperUrl} rel="noreferrer" target="_blank">Paper <ArrowUpRight size={13} /></a>
              <a href={method.sourceUrl} rel="noreferrer" target="_blank">Source <GitBranch size={13} /></a>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}
