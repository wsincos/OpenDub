import { useState } from "react";
import { ArrowLeft, ArrowUpRight, BookOpen, ChevronRight, Code2, Eye, FolderPlus, Pin, Waves } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { englishIndefiniteArticle, getMethod, GraphPosition, MethodNode } from "../../content/methods";
import { MethodConceptPanel } from "./concepts/MethodConceptPanel";
import "./concepts/method-concepts.css";
import "./method-canvas.css";
import { PaperArchitectureFigure } from "./PaperArchitectureFigure";

const chapters = ["Overview", "Flow", "Signals", "Evidence"] as const;
const chapterDescriptions = {
  Overview: "Follow the main path while retaining the method's common inputs.",
  Flow: "Inspect every paper-defined branch and where it rejoins the complete method.",
  Signals: "Select a component, then pin only its declared observable signals.",
  Evidence: "All component descriptions trace back to the fixed paper and source revision.",
} as const;

export function MethodCanvasPage() {
  const { methodSlug } = useParams();
  const method = getMethod(methodSlug);
  const [selectedId, setSelectedId] = useState(method?.overviewNodeIds[0] ?? "");
  const [chapter, setChapter] = useState<(typeof chapters)[number]>("Flow");
  const [pinned, setPinned] = useState<string[]>([]);

  if (!method) return <main className="method-not-found"><h1>Method not found</h1><Link to="/methods">Return to Methods</Link></main>;

  const activeMethod = method;
  const overviewIds = new Set([...activeMethod.overviewNodeIds, ...activeMethod.nodes.filter((node) => isInputNode(node)).map((node) => node.id)]);
  const visibleNodes = activeMethod.nodes.filter((node) => chapter === "Overview" ? overviewIds.has(node.id) : true);
  const visibleNodeIds = new Set(visibleNodes.map((node) => node.id));
  const visibleEdges = activeMethod.edges.filter((edge) => visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target));
  const selected = visibleNodes.find((node) => node.id === selectedId) ?? visibleNodes[0];
  const selectedIndex = activeMethod.nodes.findIndex((node) => node.id === selected.id);
  const selectedEdges = new Set(visibleEdges.filter((edge) => edge.source === selected.id || edge.target === selected.id).map((edge) => edge.id));
  const connectedNodeIds = new Set(visibleEdges.filter((edge) => edge.source === selected.id || edge.target === selected.id).flatMap((edge) => [edge.source, edge.target]));

  function togglePinned(signal: string) {
    setPinned((current) => current.includes(signal) ? current.filter((value) => value !== signal) : [...current, signal]);
  }

  function selectChapter(nextChapter: (typeof chapters)[number]) {
    setChapter(nextChapter);
    const nextNodes = activeMethod.nodes.filter((node) => nextChapter === "Overview" ? overviewIds.has(node.id) : true);
    if (!nextNodes.some((node) => node.id === selectedId)) setSelectedId(nextNodes[0]?.id ?? "");
  }

  return (
    <main className="method-canvas-page" style={{ "--method-color": method.color } as React.CSSProperties}>
      <header className="method-canvas-header">
        <Link className="back-link" to="/methods"><ArrowLeft size={15} /> All methods</Link>
        <div className="method-title"><span>{method.teamLabel}</span><h1>{method.title}</h1><p>{method.originalFocus}</p></div>
        <div className="header-status"><span><i /> {method.status}</span><Link aria-label={`Prepare ${englishIndefiniteArticle(method.title)} ${method.title} project`} className="prepare-project" to={`/studio?method=${method.slug}`}><FolderPlus size={14} /> Prepare project</Link><a aria-label={`Open published record for ${method.title}`} href={method.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={14} /> PUBLISHED RECORD <ArrowUpRight size={13} /></a></div>
      </header>

      <PaperArchitectureFigure method={method} />

      <section className="canvas-layout">
        <aside className="method-chapters" aria-label="Method detail chapters">
          {chapters.map((item) => <button className={chapter === item ? "is-active" : ""} key={item} onClick={() => selectChapter(item)} type="button">{item}</button>)}
          <div className="chapter-rule" />
          <p>COMPLETE METHOD</p>
          <span>{method.id}</span>
        </aside>

        <section className="method-graph-area" aria-label={`${method.title} complete method graph`}>
          <div className="graph-topbar"><span><Eye size={14} /> {chapter.toUpperCase()} VIEW</span><span>{chapterDescriptions[chapter]}</span></div>
          <div className="method-graph">
            <svg aria-hidden="true" className="graph-lines" viewBox="0 0 1000 460" preserveAspectRatio="none">
              {visibleEdges.map((edge) => {
                const source = method.positions[edge.source];
                const target = method.positions[edge.target];
                return <path className={selectedEdges.has(edge.id) ? "is-lit" : ""} d={graphPath(source, target)} data-edge-id={edge.id} key={edge.id} />;
              })}
            </svg>
            <div className="graph-nodes">
              {visibleNodes.map((node) => {
                const position = method.positions[node.id];
                const nodeIndex = method.nodes.findIndex((item) => item.id === node.id);
                return (
                <button
                  aria-label={`Inspect ${node.label}`}
                  aria-pressed={selected.id === node.id}
                  className={`graph-node ${node.tone} ${selected.id === node.id ? "is-selected" : ""} ${connectedNodeIds.has(node.id) ? "is-connected" : ""}`}
                  key={node.id}
                  onClick={() => setSelectedId(node.id)}
                  style={{ left: `${position.x}%`, top: `${position.y}%` }}
                  type="button"
                >
                  <span>{nodeIndex + 1}</span><strong>{node.short}</strong><small>{node.label}</small>
                </button>
              )})}
            </div>
          <div className="graph-caption"><span>COMMON INPUTS</span><span>ORIGINAL METHOD FLOW</span><span>TARGET SPEECH</span></div>
          </div>
          <div className="method-story"><b>{method.contribution}</b><span>Each node keeps its original method role. OpenDub only standardizes how it is explored.</span></div>
        </section>

        <aside className="node-inspector" aria-label="Selected method component inspector">
          <div className="inspector-kicker"><span>COMPONENT INSPECTOR</span><em>0{selectedIndex + 1} / 0{method.nodes.length}</em></div>
          <p className={`node-tone ${selected.tone}`}>{selected.short}</p>
          <h2>{selected.label}</h2>
          <p className="node-detail">{selected.detail}</p>
          <div className="node-section"><span>OBSERVABLE SIGNALS</span><div className="signal-chips">{selected.signals.map((signal) => <button className={pinned.includes(signal) ? "is-pinned" : ""} key={signal} onClick={() => togglePinned(signal)} type="button"><Pin size={12} /> {signal}</button>)}</div></div>
          <div className="node-section"><span>VIEW MODE</span><p className="mode-description"><i /> Concept explanation. Signals are illustrative unless a Replay or Live bundle is attached.</p></div>
          <div className="inspector-actions"><a aria-label={`Open published record for ${method.title}`} href={method.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={14} /> PUBLISHED RECORD</a><a href={method.sourceUrl} rel="noreferrer" target="_blank"><Code2 size={14} /> Source</a><Link to="/evidence">Evidence</Link></div>
        </aside>
      </section>

      <MethodConceptPanel methodSlug={method.slug} />

      <section className="signal-dock" aria-label="Pinned signals">
        <div className="signal-dock-heading"><span><Waves size={16} /> SIGNAL DOCK</span><p>{pinned.length ? `${pinned.length} signal${pinned.length > 1 ? "s" : ""} pinned` : "Pin any component signal to compare it on the common time axis."}</p></div>
        <div className="signal-dock-content">
          {pinned.length ? pinned.map((signal, index) => <SignalStrip index={index} key={signal} onRemove={() => togglePinned(signal)} signal={signal} />) : <div className="signal-empty">Select a component, then pin a signal. The dock uses one shared timeline, without pretending every internal tensor is observable.</div>}
        </div>
      </section>
    </main>
  );
}

function SignalStrip({ index, onRemove, signal }: { index: number; onRemove: () => void; signal: string }) {
  return <div className="signal-strip"><span>{signal.toUpperCase()}</span><div className={`signal-art signal-${index % 3}`}>{Array.from({ length: 30 }, (_, item) => <i key={item} style={{ height: `${20 + ((item * (index + 7)) % 70)}%` }} />)}</div><button aria-label={`Remove ${signal}`} onClick={onRemove} type="button">×</button></div>;
}

function isInputNode(node: MethodNode) {
  return ["Video", "Text", "Reference"].includes(node.short);
}

function graphPath(source: GraphPosition, target: GraphPosition) {
  const startX = source.x * 10;
  const startY = source.y * 4.6;
  const endX = target.x * 10;
  const endY = target.y * 4.6;
  const curve = Math.max(36, Math.abs(endX - startX) * 0.44);
  return `M${startX} ${startY} C${startX + curve} ${startY}, ${endX - curve} ${endY}, ${endX} ${endY}`;
}
