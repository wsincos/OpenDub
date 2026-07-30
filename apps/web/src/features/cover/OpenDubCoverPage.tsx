import { AudioLines, Film, Subtitles } from "lucide-react";

import "./open-dub-cover.css";

const inputs = [
  { Icon: Film, label: "VIDEO", className: "is-video" },
  { Icon: Subtitles, label: "TEXT", className: "is-text" },
  { Icon: AudioLines, label: "REFERENCE SPEECH", className: "is-reference" },
] as const;

export function OpenDubCoverPage() {
  return (
    <main className="open-dub-cover" aria-label="OpenDub presentation cover">
      <div aria-hidden="true" className="cover-grid" />
      <div aria-hidden="true" className="cover-axis cover-axis-left" />
      <div aria-hidden="true" className="cover-axis cover-axis-right" />

      <header className="cover-header">
        <span className="cover-mark">OD</span>
        <span>OPEN-SOURCE RESEARCH PLATFORM</span>
        <time>00:00 / 00:07</time>
      </header>

      <section className="cover-identity" aria-labelledby="cover-wordmark">
        <p>OPEN DUB / RESEARCH INTERFACE</p>
        <h1 id="cover-wordmark">OpenDub</h1>
        <strong>MULTIMODAL INTELLIGENT VIDEO DUBBING</strong>
        <span>MAKE VIDEO DUBBING INTELLIGIBLE.</span>
      </section>

      <section aria-label="OpenDub input signal convergence" className="cover-convergence">
        <div className="cover-input-signals">
          {inputs.map(({ Icon, className, label }) => (
            <div className={className} key={label}>
              <Icon aria-hidden="true" size={14} />
              <span>{label}</span>
            </div>
          ))}
        </div>
        <div aria-hidden="true" className="cover-signal-rail">
          <i className="cover-packet cover-packet-video" />
          <i className="cover-packet cover-packet-text" />
          <i className="cover-packet cover-packet-reference" />
          <b>RESOLVE</b>
        </div>
        <div className="cover-output-signal">
          <span>DUBBED VIDEO</span>
          <small>TIMING / IDENTITY / EXPRESSION</small>
        </div>
      </section>

      <footer className="cover-footer">
        <span>VIDEO / TEXT / REFERENCE SPEECH</span>
        <span>OPEN SOURCE / INTERACTIVE / MULTIMODAL</span>
      </footer>
    </main>
  );
}
