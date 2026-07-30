import { ImageIcon, ScanLine } from "lucide-react";

import type { ShowcaseArtifact, ShowcaseCase } from "../../content/showcases";
import { type AudioFeature, useAudioFeature } from "../vtts/useAudioFeature";

type ArchiveAcousticViewProps = {
  activeArtifact: ShowcaseArtifact;
  activeCase: ShowcaseCase;
  currentTime: number;
  onSeek: (time: number) => void;
};

type TraceChartProps = {
  currentTime: number;
  durationSeconds: number;
  feature: AudioFeature | null;
  kind: "energy" | "f0";
  label: string;
};

export function ArchiveAcousticView({ activeArtifact, activeCase, currentTime, onSeek }: ArchiveAcousticViewProps) {
  const feature = useAudioFeature(activeArtifact.featureUrl);
  const cursor = `${Math.min(100, Math.max(0, currentTime / activeCase.durationSeconds * 100))}%`;
  const frameTimes = [0, 0.25, 0.5, 0.75, 1].map((fraction) => Math.min(activeCase.durationSeconds * fraction, Math.max(0, activeCase.durationSeconds - 1 / 25)));
  const selectedFrame = Math.min(4, Math.floor(currentTime / activeCase.durationSeconds * 5));

  return (
    <section aria-label="File-derived acoustic view" className="acoustic-view">
      <div className="compare-section-heading"><span>FILE-DERIVED ACOUSTIC VIEW</span><small>SELECTED RECORDING ONLY · NOT MODEL INTERNALS</small></div>
      <div className="acoustic-view-grid">
        <div className="acoustic-mel-panel">
          <div className="acoustic-panel-label"><span>LOG-MEL / SELECTED ARCHIVE AUDIO</span><small>DERIVED FROM THE SELECTED FILE</small></div>
          <div className="acoustic-mel-image">
            <img alt={`Log-mel spectrogram derived from ${activeCase.displayName} ${activeArtifact.label} archive audio`} src={activeArtifact.melUrl} />
            <span aria-hidden="true" className="acoustic-cursor" style={{ left: cursor }} />
          </div>
        </div>
        <div className="acoustic-trace-stack">
          <TraceChart currentTime={currentTime} durationSeconds={activeCase.durationSeconds} feature={feature} kind="f0" label="F0 CONTOUR / UNVOICED GAPS RETAINED" />
          <TraceChart currentTime={currentTime} durationSeconds={activeCase.durationSeconds} feature={feature} kind="energy" label="ENERGY CONTOUR / ANALYSIS SCALE" />
        </div>
      </div>
      <div className="acoustic-contact-section">
        <div className="acoustic-panel-label"><span><ImageIcon size={13} /> ARCHIVE FRAME CONTACTS</span><small>CLICK A FRAME TO SEEK WITHOUT PLAYBACK</small></div>
        <div className="acoustic-contact-strip">
          {activeArtifact.contactFrameUrls.map((url, index) => (
            <button
              aria-current={index === selectedFrame ? "true" : undefined}
              aria-label={`Seek ${activeArtifact.label} archive frame ${index + 1}`}
              className={index === selectedFrame ? "is-active" : ""}
              key={url}
              onClick={() => onSeek(frameTimes[index] ?? 0)}
              type="button"
            >
              <img alt="" src={url} />
              <span>{formatTime(frameTimes[index] ?? 0)}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="acoustic-file-readout">
        <span><ScanLine size={13} /> ARCHIVE RECORD / SELECTED FILE</span>
        <dl>
          <div><dt>SELECTED FILE</dt><dd>{activeArtifact.path}</dd></div>
          <div><dt>CONTAINER</dt><dd>{formatTime(activeCase.durationSeconds)} · archived source</dd></div>
          <div><dt>SOURCE HASH</dt><dd>{activeArtifact.sha256}</dd></div>
          <div><dt>FEATURE DERIVATION</dt><dd>FFmpeg PCM → peaks / mel / F0 / energy / contacts</dd></div>
        </dl>
      </div>
    </section>
  );
}

function TraceChart({ currentTime, durationSeconds, feature, kind, label }: TraceChartProps) {
  const values = kind === "f0" ? feature?.f0_hz : feature?.energy;
  const path = values ? tracePath(values) : "";
  const cursor = `${Math.min(100, Math.max(0, currentTime / durationSeconds * 100))}%`;

  return (
    <div className="acoustic-trace-panel">
      <div className="acoustic-panel-label"><span>{label}</span><small>{kind === "energy" ? "ANALYSIS SCALE" : "HERTZ"}</small></div>
      <div className="acoustic-trace-chart">
        {path ? <svg aria-label={`${label} derived from the selected archive audio`} preserveAspectRatio="none" role="img" viewBox="0 0 100 40"><path d={path} /></svg> : <div className="acoustic-empty-trace">FEATURE UNAVAILABLE</div>}
        <span aria-hidden="true" className="acoustic-cursor" style={{ left: cursor }} />
      </div>
    </div>
  );
}

function tracePath(values: Array<number | null>): string {
  const defined = values.filter((value): value is number => typeof value === "number" && Number.isFinite(value));
  if (defined.length < 2) return "";
  const minimum = Math.min(...defined);
  const maximum = Math.max(...defined);
  const range = Math.max(0.00001, maximum - minimum);
  let started = false;
  return values.map((value, index) => {
    if (value === null || !Number.isFinite(value)) {
      started = false;
      return "";
    }
    const x = values.length === 1 ? 0 : index / (values.length - 1) * 100;
    const y = 36 - (value - minimum) / range * 32;
    const command = started ? "L" : "M";
    started = true;
    return `${command}${x.toFixed(3)} ${y.toFixed(3)}`;
  }).join(" ");
}

function formatTime(value: number) {
  return `00:${value.toFixed(3).padStart(6, "0")}`;
}
