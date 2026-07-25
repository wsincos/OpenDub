import type { CSSProperties } from "react";
import { AudioLines, Check, FileText, Film, LockKeyhole, ScanSearch, ShieldCheck, Waves } from "lucide-react";

import "./comparison-lab.css";

const candidates = [
  { name: "HPMDubbing", venue: "CVPR 2023", color: "#1877c9", focus: "Hierarchical visual prosody" },
  { name: "StyleDubber", venue: "ACL Findings 2024", color: "#7656c1", focus: "Multi-scale style learning" },
  { name: "EmoDubber", venue: "CVPR 2025", color: "#c84b61", focus: "Controllable emotional dubbing" },
];

export function ComparisonLabPage() {
  return (
    <main className="comparison-lab">
      <header className="comparison-intro">
        <div>
          <p className="eyebrow">COMPARISON LAB / EVIDENCE-GATED</p>
          <h1>Comparisons need the same scene.</h1>
          <p>A result earns a place here only after its video, text, reference speech, rights, and timing all bind to one published case.</p>
        </div>
        <div className="gate-status" aria-label="Comparison admission status"><span><LockKeyhole size={14} /> GATE CLOSED</span><small>0 / 3 verified replay bundles</small></div>
      </header>

      <section className="comparison-grid">
        <section className="common-case" aria-label="Common input case">
          <div className="case-heading"><span>COMMON INPUT CASE</span><em>CONCEPT / NOT ADMITTED</em></div>
          <div className="case-scene">
            <img alt="Fictional actor used only for the OpenDub concept case" src="/atlas/demo/scene-v1.png" />
            <span><Film size={14} /> VIDEO PREVIEW</span>
          </div>
          <div className="case-inputs">
            <CaseCondition icon={<Film size={15} />} label="Video" value="Concept scene asset" />
            <CaseCondition icon={<FileText size={15} />} label="Text" value="“你终于来了。”" />
            <CaseCondition icon={<AudioLines size={15} />} label="Reference speech" value="No public track attached" />
          </div>
        </section>

        <section className="admission-panel" aria-label="Comparison admission checks">
          <div className="case-heading"><span>CASE HANDSHAKE</span><em>REQUIRED BEFORE RANKING</em></div>
          <div className="admission-list">
            <AdmissionCheck label="Video fingerprint" state="Awaiting authorized replay case" />
            <AdmissionCheck label="Text fingerprint" state="Awaiting case manifest" />
            <AdmissionCheck label="Reference speech rights" state="No redistributable asset attached" />
            <AdmissionCheck label="Timebase and loudness policy" state="Defined, no result bundle yet" />
          </div>
          <div className="admission-footer"><ShieldCheck size={17} /><span>Only a verified common case can unlock synchronized listening and metrics.</span></div>
        </section>
      </section>

      <section className="candidate-section" aria-label="Candidate method results">
        <div className="candidate-heading"><div><p>RESULT CANDIDATES</p><h2>Three complete methods. Zero invented outputs.</h2></div><span><ScanSearch size={15} /> Evidence room</span></div>
        <div className="candidate-list">
          {candidates.map((candidate, index) => (
            <article className="candidate-row" key={candidate.name} style={{ "--candidate": candidate.color } as CSSProperties}>
              <div className="candidate-index">0{index + 1}</div>
              <div className="candidate-method"><strong>{candidate.name}</strong><span>{candidate.venue} · {candidate.focus}</span></div>
              <div className="candidate-signal" aria-label={`${candidate.name} replay signal unavailable`}><Waves size={15} /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /></div>
              <div className="candidate-proof"><span>No public replay bundle</span><small>Source, weights, input case, and rights must verify together.</small></div>
              <button disabled type="button">Replay unavailable</button>
            </article>
          ))}
        </div>
      </section>

      <section className="metric-surface" aria-label="Comparable result metrics">
        <div><p>COMPARABLE METRICS</p><h2>Metrics remain unavailable until their preprocessing agrees.</h2></div>
        <div className="metric-columns"><Metric label="Lip synchronization" /><Metric label="Pronunciation" /><Metric label="Speaker / style" /><Metric label="Emotion control" /></div>
      </section>
    </main>
  );
}

function CaseCondition({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return <div className="case-condition"><span>{icon}</span><div><small>{label}</small><strong>{value}</strong></div></div>;
}

function AdmissionCheck({ label, state }: { label: string; state: string }) {
  return <div className="admission-check"><span><Check size={14} /></span><div><strong>{label}</strong><small>{state}</small></div><em>Pending</em></div>;
}

function Metric({ label }: { label: string }) {
  return <div className="metric-column"><span>{label}</span><strong>N/A</strong><small>Not comparable</small></div>;
}
