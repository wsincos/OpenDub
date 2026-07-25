import { useState } from "react";
import { ArrowLeft, ArrowUpRight, BookOpen, ChevronRight, Code2, Eye, Pin, Waves } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { getMethod, MethodNode } from "../../content/methods";
import "./method-canvas.css";

const chapters = ["Overview", "Flow", "Signals", "Evidence"] as const;

export function MethodCanvasPage() {
  const { methodSlug } = useParams();
  const method = getMethod(methodSlug);
  const [selectedId, setSelectedId] = useState(method?.nodes[0]?.id ?? "");
  const [chapter, setChapter] = useState<(typeof chapters)[number]>("Flow");
  const [pinned, setPinned] = useState<string[]>([]);

  if (!method) return <main className="method-not-found"><h1>Method not found</h1><Link to="/methods">Return to Methods</Link></main>;

  const selected = method.nodes.find((node) => node.id === selectedId) ?? method.nodes[0];
  const selectedIndex = method.nodes.findIndex((node) => node.id === selected.id);

  function togglePinned(signal: string) {
    setPinned((current) => current.includes(signal) ? current.filter((value) => value !== signal) : [...current, signal]);
  }

  return (
    <main className="method-canvas-page" style={{ "--method-color": method.color } as React.CSSProperties}>
      <header className="method-canvas-header">
        <Link className="back-link" to="/methods"><ArrowLeft size={15} /> All methods</Link>
        <div className="method-title"><span>{method.venue} {method.year}</span><h1>{method.title}</h1><p>{method.question}</p></div>
        <div className="header-status"><span><i /> {method.status}</span><a href={method.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={14} /> Paper <ArrowUpRight size={13} /></a></div>
      </header>

      <section className="canvas-layout">
        <aside className="method-chapters" aria-label="Method detail chapters">
          {chapters.map((item) => <button className={chapter === item ? "is-active" : ""} key={item} onClick={() => setChapter(item)} type="button">{item}</button>)}
          <div className="chapter-rule" />
          <p>COMPLETE METHOD</p>
          <span>{method.id}</span>
        </aside>

        <section className="method-graph-area" aria-label={`${method.title} complete method graph`}>
          <div className="graph-topbar"><span><Eye size={14} /> {chapter.toUpperCase()} VIEW</span><span>Click a component to inspect its evidence-bound signals.</span></div>
          <div className="method-graph">
            <svg aria-hidden="true" className="graph-lines" viewBox="0 0 1000 360" preserveAspectRatio="none">
              {method.nodes.slice(0, -1).map((node, index) => <path className={index <= selectedIndex ? "is-lit" : ""} d={`M${110 + index * 158} ${180 + (index % 2 ? 52 : -52)} C${160 + index * 158} ${180 + (index % 2 ? 52 : -52)}, ${196 + index * 158} ${180 + ((index + 1) % 2 ? 52 : -52)}, ${250 + index * 158} ${180 + ((index + 1) % 2 ? 52 : -52)}`} key={node.id} />)}
            </svg>
            <div className="graph-nodes">
              {method.nodes.map((node, index) => (
                <button
                  aria-pressed={selected.id === node.id}
                  className={`graph-node ${node.tone} ${selected.id === node.id ? "is-selected" : ""} ${index <= selectedIndex ? "is-visited" : ""}`}
                  key={node.id}
                  onClick={() => setSelectedId(node.id)}
                  style={{ left: `${11 + index * 15.8}%`, top: `${index % 2 ? 56 : 24}%` }}
                  type="button"
                >
                  <span>{index + 1}</span><strong>{node.short}</strong><small>{node.label}</small>
                </button>
              ))}
            </div>
            <div className="graph-caption"><span>INPUT CONDITIONS</span><span>METHOD-INTERNAL TRANSFORMATIONS</span><span>TARGET SPEECH</span></div>
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
          <div className="inspector-actions"><a href={method.paperUrl} rel="noreferrer" target="_blank"><BookOpen size={14} /> Paper section</a><a href={method.sourceUrl} rel="noreferrer" target="_blank"><Code2 size={14} /> Source</a></div>
        </aside>
      </section>

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
