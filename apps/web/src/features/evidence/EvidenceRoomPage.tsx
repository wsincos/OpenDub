import type { CSSProperties, ReactNode } from "react";
import { BookOpen, CheckCircle2, CircleAlert, ExternalLink, FileKey2, Fingerprint, GitCommitHorizontal, LockKeyhole, TerminalSquare } from "lucide-react";

import { methods, MethodDefinition } from "../../content/methods";
import "./evidence-room.css";

const auditNotes: Record<MethodDefinition["id"], string> = {
  "galaxycong/hpmdubbing": "Feature-file workflow and restricted upstream media still require an authorized fixture.",
  "galaxycong/styledubber": "Dataset-specific features still need a reproducible preprocessing record.",
  "galaxycong/emodubber": "Published basic inference is not an admitted public runtime; emotion inference remains unadmitted.",
};

const auditFiles: Record<MethodDefinition["id"], string> = {
  "galaxycong/hpmdubbing": "hpmdubbing-f50dfa7.md",
  "galaxycong/styledubber": "styledubber-bc431c8.md",
  "galaxycong/emodubber": "emodubber-553fa054.md",
};

export function EvidenceRoomPage() {
  return (
    <main className="evidence-room">
      <header className="evidence-intro">
        <div>
          <p><Fingerprint size={13} /> EVIDENCE OBSERVATORY</p>
          <h1>A source record is not yet a runnable method.</h1>
          <span>Every complete method remains connected to its published record, pinned source revision, code license, and an explicit runtime boundary. The source trail is readable; runtime admission is separate.</span>
        </div>
        <div className="evidence-summary" aria-label="Method provenance summary"><strong>3 SOURCE RECORDS / 0 ADMITTED RUNTIMES</strong><span>PUBLIC STATE · CONCEPT ATLAS + ARCHIVED EXAMPLES</span></div>
      </header>

      <section className="evidence-source-lines" aria-label="Method source lines">
        <div className="source-lines-heading"><span>METHOD SOURCE LINES</span><span>PUBLISHED RECORD → PINNED REVISION → RUNTIME BOUNDARY</span></div>
        {methods.map((method, index) => <MethodEvidenceRow index={index} key={method.id} method={method} />)}
      </section>

      <section className="admission-chain" aria-label="Runtime admission rail">
        <div className="admission-copy"><p>RUNTIME ADMISSION RAIL</p><h2>A published file is not a runnable method.</h2><span>OpenDub advances one complete method only when all evidence stages are present together.</span></div>
        <div className="admission-stages">
          <AdmissionStage icon={<CheckCircle2 size={16} />} label="Source revision" state="Pinned" tone="verified" />
          <AdmissionStage icon={<CheckCircle2 size={16} />} label="Code license" state="Verified" tone="verified" />
          <AdmissionStage icon={<FileKey2 size={16} />} label="Weight terms" state="Missing" tone="blocked" />
          <AdmissionStage icon={<Fingerprint size={16} />} label="SHA-256" state="Missing" tone="blocked" />
          <AdmissionStage icon={<TerminalSquare size={16} />} label="Isolated smoke" state="Not run" tone="blocked" />
          <AdmissionStage icon={<LockKeyhole size={16} />} label="Public replay" state="Not admitted" tone="blocked" />
        </div>
      </section>

      <section className="evidence-boundary" aria-label="Current public content boundary">
        <CircleAlert size={18} />
        <div><strong>Current public boundary: Concept Atlas and authorized historical examples.</strong><span>Concept visuals explain reviewed method relationships. They do not imply a checkpoint, a generated audio result, or a public Replay bundle.</span></div>
      </section>
    </main>
  );
}

function MethodEvidenceRow({ index, method }: { index: number; method: MethodDefinition }) {
  const auditUrl = `https://github.com/wsincos/OpenDub/blob/main/docs/audits/${auditFiles[method.id]}`;
  const commit = method.sourceCommit.slice(0, 7);
  return (
    <article className="evidence-source-line" style={{ "--method-color": method.color } as CSSProperties}>
      <div className="evidence-method"><span>{String(index + 1).padStart(2, "0")}</span><div><p>{method.teamLabel}</p><h2>{method.title}</h2><small>{method.originalFocus}</small></div></div>
      <div className="evidence-rail" aria-label={`${method.title} source evidence`}>
        <EvidenceFact icon={<BookOpen size={14} />} label="PUBLISHED RECORD" value="Primary source" href={method.paperUrl} />
        <EvidenceFact icon={<GitCommitHorizontal size={14} />} label="PINNED REVISION" value={commit} href={method.sourceUrl} linkLabel={`Open ${method.title} source at ${commit}`} />
        <EvidenceFact icon={<CheckCircle2 size={14} />} label="CODE LICENSE" value={method.sourceLicense} tone="verified" />
        <EvidenceFact icon={<FileKey2 size={14} />} label="WEIGHT TERMS" value="Weight terms not verified" tone="blocked" />
        <EvidenceFact icon={<TerminalSquare size={14} />} label="RUNTIME" value={`Runtime ${method.runtimeStatus}`} tone="blocked" />
        <EvidenceFact icon={<LockKeyhole size={14} />} label="PUBLIC CONTENT" value="Concept only" tone="concept" />
      </div>
      <footer className="evidence-line-footer"><p>{auditNotes[method.id]}</p><a href={auditUrl} rel="noreferrer" target="_blank">AUDIT NOTE <ExternalLink size={13} /></a></footer>
    </article>
  );
}

function EvidenceFact({ href, icon, label, linkLabel, tone, value }: { href?: string; icon: ReactNode; label: string; linkLabel?: string; tone?: "verified" | "blocked" | "concept"; value: string }) {
  const content = <><span>{icon}{label}</span><strong className={tone ? `is-${tone}` : ""}>{value}{href ? <ExternalLink size={11} /> : null}</strong></>;
  return href ? <a aria-label={linkLabel} className="evidence-fact" href={href} rel="noreferrer" target="_blank">{content}</a> : <div className="evidence-fact">{content}</div>;
}

function AdmissionStage({ icon, label, state, tone }: { icon: ReactNode; label: string; state: string; tone: "verified" | "blocked" }) {
  return <div className={`admission-stage is-${tone}`}><span>{icon}</span><div><small>{label}</small><strong>{state}</strong></div></div>;
}
