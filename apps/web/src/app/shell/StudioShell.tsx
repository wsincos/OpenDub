import {
  ChevronDown,
  Download,
  FileAudio,
  Film,
  Layers3,
  MoreHorizontal,
  Pause,
  Play,
  Redo2,
  ShieldCheck,
  SlidersHorizontal,
  Undo2,
  Waves,
} from "lucide-react";

import "./studio-shell.css";

const timelineMarks = ["00:00", "00:02", "00:04", "00:06", "00:08", "00:10"];

export function StudioShell() {
  return (
    <main className="studio" aria-label="OpenDub Studio">
      <header className="topbar">
        <div className="brand" aria-label="OpenDub">
          <span className="brand-mark">OD</span>
          <span>OpenDub</span>
          <span className="brand-divider" />
          <span className="project-name">Authorized Demo</span>
          <ChevronDown aria-hidden="true" size={15} />
        </div>
        <div className="save-state"><span className="state-dot" /> Saved locally</div>
        <div className="topbar-actions">
          <IconButton label="Undo"><Undo2 size={17} /></IconButton>
          <IconButton label="Redo"><Redo2 size={17} /></IconButton>
          <button className="check-button"><ShieldCheck size={16} /> Run checks</button>
          <button className="export-button"><Download size={16} /> Export</button>
        </div>
      </header>

      <aside className="left-panel">
        <PanelHeading icon={<Layers3 size={16} />} title="Project" />
        <nav className="asset-nav" aria-label="Project resources">
          <Resource label="Video" detail="demo_take_01.mp4" icon={<Film size={16} />} active />
          <Resource label="Dialogue" detail="4 segments" icon={<Waves size={16} />} />
          <Resource label="Voice" detail="Authorized" icon={<FileAudio size={16} />} />
          <Resource label="Models" detail="0 ready" icon={<SlidersHorizontal size={16} />} />
        </nav>
        <div className="asset-note">
          <ShieldCheck size={15} />
          <span>Voice consent recorded</span>
        </div>
      </aside>

      <section className="workspace">
        <div className="video-toolbar">
          <span className="eyebrow">PROGRAM MONITOR</span>
          <span className="timecode">00:00:03:12</span>
          <button className="icon-button" aria-label="More monitor options" title="More monitor options"><MoreHorizontal size={18} /></button>
        </div>
        <div className="monitor" aria-label="Video preview">
          <div className="monitor-frame">
            <div className="subject-shape" />
            <div className="monitor-guides"><span /><span /></div>
            <p className="subtitle-preview">You finally made it.</p>
          </div>
        </div>
        <div className="transport" aria-label="Playback controls">
          <button className="play-button" aria-label="Play" title="Play"><Play fill="currentColor" size={17} /></button>
          <button className="icon-button" aria-label="Pause" title="Pause"><Pause size={17} /></button>
          <span className="transport-time">00:00:03.120 / 00:00:11.200</span>
          <span className="transport-mode">Proxy · 720p</span>
        </div>
        <Timeline />
      </section>

      <aside className="inspector">
        <PanelHeading icon={<SlidersHorizontal size={16} />} title="Segment inspector" />
        <label className="field-label" htmlFor="dialogue">Dialogue</label>
        <textarea id="dialogue" className="dialogue" defaultValue="You finally made it." rows={3} />
        <div className="field-grid">
          <div><span className="field-label">Character</span><button className="select-field">Lin <ChevronDown size={14} /></button></div>
          <div><span className="field-label">Target</span><span className="mono-value">1.20 s</span></div>
        </div>
        <div className="inspector-section">
          <div className="section-title"><span>Emotion direction</span><span className="planned-badge">Planned adapter</span></div>
          <div className="emotion-row" aria-label="Emotion labels"><button className="emotion selected">Happy</button><button className="emotion">Neutral</button><button className="emotion">Sad</button></div>
          <div className="range-heading"><span>Intensity</span><output>0.82</output></div>
          <input aria-label="Emotion intensity" className="range" type="range" min="0" max="1" step="0.01" defaultValue="0.82" />
        </div>
        <div className="inspector-section capability-note">
          <span className="field-label">Model capability</span>
          <p>Connect a verified adapter to enable generation controls.</p>
        </div>
        <button className="generate-button" disabled title="A verified adapter is required"><Waves size={17} /> Generate candidates</button>
      </aside>

      <section className="job-drawer" aria-label="Local task queue">
        <div className="drawer-title"><span>Local queue</span><span className="queue-count">0 jobs</span></div>
        <div className="queue-empty">No active jobs. Generation remains local to this workspace.</div>
      </section>
    </main>
  );
}

function IconButton({ children, label }: { children: React.ReactNode; label: string }) {
  return <button className="icon-button" aria-label={label} title={label}>{children}</button>;
}

function PanelHeading({ icon, title }: { icon: React.ReactNode; title: string }) {
  return <h2 className="panel-heading">{icon}<span>{title}</span></h2>;
}

function Resource({ active = false, detail, icon, label }: { active?: boolean; detail: string; icon: React.ReactNode; label: string }) {
  return <button className={`resource ${active ? "active" : ""}`}><span className="resource-icon">{icon}</span><span><strong>{label}</strong><small>{detail}</small></span></button>;
}

function Timeline() {
  return <section className="timeline" aria-label="Dubbing timeline">
    <div className="timeline-header"><span>Timeline</span><span className="mono-value">24 fps · 48 kHz</span></div>
    <div className="ruler">{timelineMarks.map((mark) => <span key={mark}>{mark}</span>)}</div>
    <div className="track"><span className="track-label">Original</span><div className="waveform original-wave" /></div>
    <div className="track"><span className="track-label">Dialogue</span><div className="segment-block"><span>Lin · You finally made it.</span><small>00:02.60 → 00:03.80</small></div></div>
    <div className="track"><span className="track-label">Candidate</span><div className="empty-track">Select a verified adapter to generate candidates</div></div>
    <div className="playhead" aria-hidden="true"><span /></div>
  </section>;
}
