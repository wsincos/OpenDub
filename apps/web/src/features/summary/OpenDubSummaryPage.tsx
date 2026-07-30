import { ArrowUpRight, BookOpenCheck, FolderKanban, GitBranch, RadioTower, Waves } from "lucide-react";
import { Link } from "react-router-dom";

import "./open-dub-summary.css";

const methods = ["HPMDubbing", "StyleDubber", "EmoDubber", "InstructDubber", "Speaker2Dub"];

const capabilities = [
  { title: "Methods", detail: "UNDERSTAND / SELECT", to: "/methods", icon: BookOpenCheck },
  { title: "Examples", detail: "HEAR ARCHIVED RESULTS", to: "/examples", icon: Waves },
  { title: "Compare", detail: "INSPECT SYNCHRONIZED EVIDENCE", to: "/compare", icon: RadioTower },
  { title: "Evidence", detail: "TRACE SOURCE BOUNDARIES", to: "/evidence", icon: GitBranch },
  { title: "Studio", detail: "PREPARE AUTHORIZED PROJECTS", to: "/studio", icon: FolderKanban },
];

export function OpenDubSummaryPage() {
  return <main className="summary-page" aria-label="OpenDub research platform summary">
    <header className="summary-header"><span>OPEN DUB / RESEARCH PLATFORM SUMMARY</span><small>OPEN DEVELOPMENT</small></header>
    <section className="summary-methods" aria-labelledby="summary-methods-heading">
      <div><p id="summary-methods-heading">TEAM-DEVELOPED COMPLETE METHODS</p><span>Original research approaches for different video-dubbing priorities.</span></div>
      <ol>{methods.map((method, index) => <li key={method}><span>{String(index + 1).padStart(2, "0")}</span><strong>{method}</strong><i aria-hidden="true" /></li>)}</ol>
    </section>
    <section className="summary-platform" aria-labelledby="summary-open-dub">
      <div aria-hidden="true" className="summary-convergence"><span /><span /><span /><span /><span /></div>
      <div className="summary-anchor"><p>OPEN-SOURCE MULTIMODAL INTELLIGENT VIDEO DUBBING PLATFORM</p><h1 id="summary-open-dub">OpenDub</h1><span>INTERACTIVE RESEARCH PLATFORM</span></div>
      <div aria-hidden="true" className="summary-distribution"><i /><i /><i /><i /><i /></div>
    </section>
    <nav aria-label="OpenDub platform capabilities" className="summary-capabilities">{capabilities.map(({ detail, icon: Icon, title, to }) => <Link key={title} to={to}><span className="summary-capability-icon"><Icon size={18} /></span><span><strong>{title}</strong><small>{detail}</small></span><ArrowUpRight aria-hidden="true" size={15} /></Link>)}</nav>
    <footer className="summary-footer"><span>TEAM RESEARCH → INTERACTIVE EVIDENCE → TRACEABLE PREPARATION</span><strong>OPEN DEVELOPMENT</strong><span>UNDERSTAND · INSPECT · PREPARE · EXTEND</span></footer>
  </main>;
}
