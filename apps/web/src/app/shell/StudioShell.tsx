import { FormEvent, ReactNode, useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowLeft,
  ChevronDown,
  FileAudio,
  FileText,
  Film,
  Layers3,
  MoreHorizontal,
  Pause,
  Play,
  ShieldCheck,
  SlidersHorizontal,
  Save,
  Trash2,
  Upload,
  Waves,
} from "lucide-react";

import {
  assetUrl,
  acceptCandidate,
  createSegment,
  createVoiceReference,
  deleteSegment,
  CandidateEvaluation,
  DubbingCandidate,
  DubbingSegment,
  EmotionLabel,
  evaluateCandidate,
  importSubtitleSegments,
  Project,
  RenderMutation,
  renderAcceptedCandidates,
  updateSegment,
  uploadAsset,
} from "../../api/client";
import "./studio-shell.css";

type StudioShellProps = { project: Project; onBack: () => void; onRefresh: () => Promise<void> };

const emotionLabels: EmotionLabel[] = ["neutral", "happy", "sad", "angry", "fearful", "surprised"];

export function StudioShell({ onBack, onRefresh, project }: StudioShellProps) {
  const [selectedSegmentId, setSelectedSegmentId] = useState<string | null>(project.segments[0]?.id ?? null);
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [evaluations, setEvaluations] = useState<Record<string, CandidateEvaluation>>({});
  const [playing, setPlaying] = useState(false);
  const [mixMode, setMixMode] = useState<RenderMutation["mix_mode"]>("remove");
  const [lastRender, setLastRender] = useState<RenderMutation | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const videoAsset = project.assets.find((asset) => asset.kind === "video");
  const audioAssets = project.assets.filter((asset) => asset.kind === "audio");
  const subtitleAssets = project.assets.filter((asset) => asset.kind === "subtitle");
  const selectedSegment = project.segments.find((segment) => segment.id === selectedSegmentId) ?? null;
  const acceptedCandidateCount = project.segments.filter((segment) => segment.accepted_candidate_id).length;
  const selectedCandidates = project.candidates.filter((candidate) => candidate.segment_id === selectedSegmentId);

  useEffect(() => {
    if (selectedSegmentId && project.segments.some((segment) => segment.id === selectedSegmentId)) return;
    setSelectedSegmentId(project.segments[0]?.id ?? null);
  }, [project.segments, selectedSegmentId]);

  const maximumEndUs = useMemo(
    () => Math.max(1_000_000, ...project.segments.map((segment) => segment.range.end_us + 500_000)),
    [project.segments],
  );

  async function refreshAfterMutation() {
    await onRefresh();
    setMessage(null);
  }

  async function submitMedia(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const file = data.get("media") as File | null;
    const kind = String(data.get("kind"));
    if (!file || file.size === 0 || !["video", "audio", "subtitle"].includes(kind)) return;
    setBusy(true);
    setMessage(null);
    try {
      await uploadAsset(project.id, file, kind as "video" | "audio" | "subtitle", project.revision);
      form.reset();
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not store this local file.");
    } finally {
      setBusy(false);
    }
  }

  async function togglePlayback() {
    if (!videoRef.current) return;
    if (videoRef.current.paused) await videoRef.current.play();
    else videoRef.current.pause();
  }

  async function submitVoiceReference(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const assetId = String(data.get("audio_asset") ?? "");
    const speakerLabel = String(data.get("speaker_label") ?? "").trim();
    const materialSource = String(data.get("material_source") ?? "");
    const allowGeneratedOutputDistribution = data.get("allow_generated_output_distribution") === "on";
    if (!assetId || !speakerLabel) return;
    setBusy(true);
    setMessage(null);
    try {
      await createVoiceReference(project.id, {
        assetId,
        speakerLabel,
        materialSource: materialSource as "self_recorded" | "licensed" | "public_domain" | "authorized_other",
        allowGeneratedOutputDistribution,
        expectedRevision: project.revision,
      });
      form.reset();
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not record the voice authorization.");
    } finally {
      setBusy(false);
    }
  }

  async function submitSegment(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const startUs = Math.round(Number(data.get("start_seconds")) * 1_000_000);
    const endUs = Math.round(Number(data.get("end_seconds")) * 1_000_000);
    const text = String(data.get("dialogue") ?? "").trim();
    if (!text || !Number.isFinite(startUs) || !Number.isFinite(endUs) || endUs <= startUs) {
      setMessage("Set a positive start and end time before adding dialogue.");
      return;
    }
    setBusy(true);
    setMessage(null);
    try {
      const created = await createSegment(project.id, {
        startUs,
        endUs,
        text,
        language: String(data.get("language") ?? "en"),
        voiceReferenceId: String(data.get("voice_reference") ?? ""),
        adapterId: "galaxycong/emodubber",
        emotionLabel: String(data.get("emotion")) as EmotionLabel,
        emotionIntensity: Number(data.get("intensity")),
        expectedRevision: project.revision,
      });
      setSelectedSegmentId(created.id);
      form.reset();
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not add the dubbing segment.");
    } finally {
      setBusy(false);
    }
  }

  async function submitSubtitleImport(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const assetId = String(data.get("subtitle_asset") ?? "");
    const voiceReferenceId = String(data.get("subtitle_voice_reference") ?? "");
    if (!assetId || !voiceReferenceId) return;
    setBusy(true);
    setMessage(null);
    try {
      const updated = await importSubtitleSegments(project.id, {
        assetId,
        language: String(data.get("subtitle_language") ?? "en"),
        voiceReferenceId,
        adapterId: "galaxycong/emodubber",
        expectedRevision: project.revision,
      });
      setSelectedSegmentId(updated.segments[0]?.id ?? null);
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not import subtitle cues.");
    } finally {
      setBusy(false);
    }
  }

  async function submitSegmentUpdate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const segmentId = String(data.get("segment_id") ?? "");
    const startUs = Math.round(Number(data.get("start_seconds")) * 1_000_000);
    const endUs = Math.round(Number(data.get("end_seconds")) * 1_000_000);
    const text = String(data.get("dialogue") ?? "").trim();
    if (!segmentId || !text || !Number.isFinite(startUs) || !Number.isFinite(endUs) || endUs <= startUs) {
      setMessage("Set a positive start and end time before saving dialogue.");
      return;
    }
    setBusy(true);
    setMessage(null);
    try {
      await updateSegment(project.id, segmentId, {
        text,
        startUs,
        endUs,
        language: String(data.get("language") ?? "en"),
        voiceReferenceId: String(data.get("voice_reference") ?? ""),
        emotionLabel: String(data.get("emotion")) as EmotionLabel,
        emotionIntensity: Number(data.get("intensity")),
        expectedRevision: project.revision,
      });
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not save the dialogue segment.");
    } finally {
      setBusy(false);
    }
  }

  async function removeSelectedSegment() {
    if (!selectedSegment || !window.confirm("Remove this dialogue segment and its candidates?")) return;
    setBusy(true);
    setMessage(null);
    try {
      await deleteSegment(project.id, selectedSegment.id, project.revision);
      setSelectedSegmentId(null);
      await refreshAfterMutation();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not remove the dialogue segment.");
    } finally {
      setBusy(false);
    }
  }

  async function reviewCandidate(candidate: DubbingCandidate, action: "accept" | "evaluate") {
    if (!selectedSegment) return;
    setBusy(true);
    setMessage(null);
    try {
      if (action === "accept") {
        await acceptCandidate(project.id, selectedSegment.id, candidate.id, project.revision);
        await refreshAfterMutation();
      } else {
        const evaluation = await evaluateCandidate(project.id, candidate.id);
        setEvaluations((current) => ({ ...current, [candidate.id]: evaluation }));
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not review this candidate.");
    } finally {
      setBusy(false);
    }
  }

  async function exportAcceptedCandidates() {
    if (!acceptedCandidateCount) return;
    setBusy(true);
    setMessage(null);
    try {
      const render = await renderAcceptedCandidates(project.id, mixMode);
      setLastRender(render);
      const download = document.createElement("a");
      download.href = render.dubbed_video_url ?? render.dubbing_audio_url;
      download.download = "";
      download.click();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not render accepted candidates.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="studio" aria-label="OpenDub Studio">
      <header className="topbar">
        <div className="brand" aria-label="OpenDub"><span className="brand-mark">OD</span><span>OpenDub</span><span className="brand-divider" /><span className="project-name">{project.name}</span><ChevronDown aria-hidden="true" size={15} /></div>
        <div className="save-state"><span className="state-dot" /> Revision {project.revision} saved locally</div>
        <div className="topbar-actions"><IconButton label="Projects" onClick={onBack}><ArrowLeft size={17} /></IconButton><select aria-label="Original audio mix" className="mix-mode" disabled={busy || !acceptedCandidateCount} onChange={(event) => setMixMode(event.target.value as RenderMutation["mix_mode"])} value={mixMode}><option value="remove">Replace original audio</option><option value="duck">Duck original audio</option><option value="preserve">Preserve original audio</option></select><button className="export-button" disabled={busy || !acceptedCandidateCount} onClick={() => void exportAcceptedCandidates()} title={acceptedCandidateCount ? "Render and download accepted candidates" : "Accept a generated candidate before exporting"}><Upload size={16} /> Export</button></div>
      </header>

      <aside className="left-panel">
        <PanelHeading icon={<Layers3 size={16} />} title="Project" />
        <nav className="asset-nav" aria-label="Project resources">
          <Resource label="Video" detail={videoAsset?.display_name ?? "Not imported"} icon={<Film size={16} />} active />
          <Resource label="Dialogue" detail={`${project.segments.length} segments`} icon={<Waves size={16} />} />
          <Resource label="Voice" detail={`${project.voice_references.length} authorized`} icon={<FileAudio size={16} />} />
          <Resource label="Models" detail="0 verified" icon={<SlidersHorizontal size={16} />} />
        </nav>
        <div className={`asset-note ${project.voice_references.length ? "" : "is-empty"}`}><ShieldCheck size={15} /><span>{project.voice_references.length ? "Voice consent recorded" : "Authorization required before generation"}</span></div>
      </aside>

      <section className="workspace">
        <div className="video-toolbar"><span className="eyebrow">PROGRAM MONITOR</span><span className="timecode">LOCAL PREVIEW</span><button className="icon-button" aria-label="More monitor options" title="More monitor options"><MoreHorizontal size={18} /></button></div>
        <div className="monitor" aria-label="Video preview">
          {videoAsset ? <video className="video-preview" controls muted onPause={() => setPlaying(false)} onPlay={() => setPlaying(true)} ref={videoRef} src={assetUrl(project.id, videoAsset.id)} /> : <div className="empty-monitor"><Film size={34} /><strong>No local video preview</strong><span>Import an authorized video in the inspector.</span></div>}
        </div>
        <div className="transport" aria-label="Playback controls"><button className="play-button" aria-label={playing ? "Pause" : "Play"} disabled={!videoAsset} onClick={() => void togglePlayback()} title={videoAsset ? (playing ? "Pause" : "Play") : "Import a local video to enable preview playback"}>{playing ? <Pause size={17} /> : <Play fill="currentColor" size={17} />}</button><span className="transport-time">{selectedSegment ? formatRange(selectedSegment) : "No selected segment"}</span><span className="transport-mode">Local workspace</span></div>
        <Timeline acceptedCandidateCount={acceptedCandidateCount} currentCandidateCount={selectedCandidates.filter((candidate) => candidate.segment_revision === selectedSegment?.revision).length} maximumEndUs={maximumEndUs} onSelect={setSelectedSegmentId} project={project} selectedSegmentId={selectedSegmentId} />
      </section>

      <aside className="inspector">
        <PanelHeading icon={<SlidersHorizontal size={16} />} title="Local setup" />
        {message ? <div className="studio-message" role="alert">{message}</div> : null}
        <form className="setup-form" onSubmit={(event) => void submitMedia(event)}>
          <span className="field-label">Source media</span><input aria-label="Local source media" name="media" required type="file" accept="video/*,audio/*,.srt,.vtt" /><select aria-label="Media kind" defaultValue="video" name="kind"><option value="video">Video</option><option value="audio">Voice audio</option><option value="subtitle">Subtitle file</option></select><button className="outline-button" disabled={busy} type="submit"><Upload size={15} /> Import locally</button>
        </form>
        {audioAssets.length > 0 && project.voice_references.length === 0 ? <form className="setup-form inspector-section" onSubmit={(event) => void submitVoiceReference(event)}><div className="section-title"><span>Voice authorization</span><ShieldCheck size={15} /></div><select aria-label="Authorized audio asset" name="audio_asset" required>{audioAssets.map((asset) => <option key={asset.id} value={asset.id}>{asset.display_name}</option>)}</select><input aria-label="Speaker label" maxLength={200} name="speaker_label" placeholder="Speaker label" required /><select aria-label="Rights source" defaultValue="self_recorded" name="material_source"><option value="self_recorded">Self recorded</option><option value="licensed">Licensed</option><option value="public_domain">Public domain</option><option value="authorized_other">Authorized other</option></select><label className="consent-check"><input aria-label="Permit output distribution" name="allow_generated_output_distribution" type="checkbox" /><span>Permit sharing generated output</span></label><button className="outline-button" disabled={busy} type="submit"><ShieldCheck size={15} /> Record authorization</button></form> : null}
        {project.voice_references.length > 0 && subtitleAssets.length > 0 ? <SubtitleImportForm busy={busy} onSubmit={submitSubtitleImport} project={project} subtitleAssets={subtitleAssets} /> : null}
        {project.voice_references.length > 0 ? <SegmentForm busy={busy} onSubmit={submitSegment} project={project} /> : <div className="inspector-section capability-note"><span className="field-label">Generation gate</span><p>Import an audio reference and record an explicit authorization before configuring dialogue.</p></div>}
        {selectedSegment ? <SegmentEditor busy={busy} onDelete={() => void removeSelectedSegment()} onSubmit={submitSegmentUpdate} project={project} segment={selectedSegment} /> : null}
        {selectedSegment ? <CandidateReview candidates={selectedCandidates} evaluations={evaluations} busy={busy} onReview={(candidate, action) => void reviewCandidate(candidate, action)} project={project} segment={selectedSegment} /> : null}
      </aside>

      <section className="job-drawer" aria-label="Local task queue"><div className="drawer-title"><span>{lastRender ? "Export" : "Local queue"}</span><span className="queue-count">{lastRender ? `r${lastRender.project_revision}` : "0 jobs"}</span></div>{lastRender ? <div className="export-result" role="status"><div><strong>Render ready</strong><span>{lastRender.distribution_authorized ? "Output sharing authorized" : "Local review only"}</span></div><nav aria-label="Rendered export files"><a href={lastRender.dubbing_audio_url}>WAV</a>{lastRender.dubbed_video_url ? <a href={lastRender.dubbed_video_url}>MP4</a> : null}<a href={lastRender.manifest_url}>Manifest</a></nav></div> : <div className="queue-empty">No model is verified in this workspace. Project setup and media remain local.</div>}</section>
    </main>
  );
}

function SegmentForm({ busy, onSubmit, project }: { busy: boolean; onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>; project: Project }) {
  return <form className="setup-form inspector-section" onSubmit={(event) => void onSubmit(event)}><div className="section-title"><span>New dialogue</span><span className="planned-badge">Planned adapter</span></div><textarea aria-label="Dialogue" name="dialogue" placeholder="Dialogue to dub" required rows={3} /><div className="compact-grid"><label>Start (s)<input defaultValue="0" min="0" name="start_seconds" required step="0.01" type="number" /></label><label>End (s)<input defaultValue="1.5" min="0.01" name="end_seconds" required step="0.01" type="number" /></label></div><select aria-label="Dialogue language" defaultValue="en" name="language"><option value="en">English</option><option value="zh">Chinese</option></select><select aria-label="Voice reference" name="voice_reference">{project.voice_references.map((reference) => <option key={reference.id} value={reference.id}>{reference.speaker_label}</option>)}</select><select aria-label="Emotion" defaultValue="neutral" name="emotion">{emotionLabels.map((emotion) => <option key={emotion} value={emotion}>{emotion}</option>)}</select><label className="range-heading">Intensity <output>0.50</output><input aria-label="Emotion intensity" defaultValue="0.5" max="1" min="0" name="intensity" step="0.05" type="range" /></label><button className="generate-button enabled" disabled={busy} type="submit"><Waves size={17} /> Add to timeline</button></form>;
}

function SubtitleImportForm({ busy, onSubmit, project, subtitleAssets }: { busy: boolean; onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>; project: Project; subtitleAssets: Project["assets"] }) {
  return <form className="setup-form inspector-section" onSubmit={(event) => void onSubmit(event)}><div className="section-title"><span>Subtitle cues</span><FileText size={15} /></div><select aria-label="Subtitle asset" name="subtitle_asset">{subtitleAssets.map((asset) => <option key={asset.id} value={asset.id}>{asset.display_name}</option>)}</select><select aria-label="Subtitle language" defaultValue="en" name="subtitle_language"><option value="en">English</option><option value="zh">Chinese</option></select><select aria-label="Subtitle voice reference" name="subtitle_voice_reference">{project.voice_references.map((reference) => <option key={reference.id} value={reference.id}>{reference.speaker_label}</option>)}</select><button className="outline-button" disabled={busy} type="submit"><FileText size={15} /> Import cues</button></form>;
}

function SegmentEditor({ busy, onDelete, onSubmit, project, segment }: { busy: boolean; onDelete: () => void; onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>; project: Project; segment: DubbingSegment }) {
  return <form className="setup-form inspector-section" key={segment.id} onSubmit={(event) => void onSubmit(event)}><div className="section-title"><span>Selected segment</span><span className="mono-value">r{segment.revision}</span></div><input name="segment_id" type="hidden" value={segment.id} /><textarea aria-label="Edit dialogue" defaultValue={segment.text} name="dialogue" required rows={3} /><div className="compact-grid"><label>Start (s)<input defaultValue={(segment.range.start_us / 1_000_000).toFixed(2)} min="0" name="start_seconds" required step="0.01" type="number" /></label><label>End (s)<input defaultValue={(segment.range.end_us / 1_000_000).toFixed(2)} min="0.01" name="end_seconds" required step="0.01" type="number" /></label></div><select aria-label="Edit language" defaultValue={segment.language} name="language"><option value="en">English</option><option value="zh">Chinese</option></select><select aria-label="Edit voice reference" defaultValue={segment.voice_reference_id} name="voice_reference">{project.voice_references.map((reference) => <option key={reference.id} value={reference.id}>{reference.speaker_label}</option>)}</select><select aria-label="Edit emotion" defaultValue={segment.emotion.label} name="emotion">{emotionLabels.map((emotion) => <option key={emotion} value={emotion}>{emotion}</option>)}</select><label className="range-heading">Intensity <output>{segment.emotion.intensity.toFixed(2)}</output><input aria-label="Edit emotion intensity" defaultValue={segment.emotion.intensity} max="1" min="0" name="intensity" step="0.05" type="range" /></label><div className="segment-actions"><button className="outline-button" disabled={busy} type="submit"><Save size={15} /> Save segment</button><button className="danger-button" disabled={busy} onClick={onDelete} type="button" title="Remove segment"><Trash2 size={15} /></button></div></form>;
}

function CandidateReview({ busy, candidates, evaluations, onReview, project, segment }: { busy: boolean; candidates: DubbingCandidate[]; evaluations: Record<string, CandidateEvaluation>; onReview: (candidate: DubbingCandidate, action: "accept" | "evaluate") => void; project: Project; segment: DubbingSegment }) {
  const reviewable = candidates.filter((candidate) => candidate.segment_revision === segment.revision || candidate.id === segment.accepted_candidate_id);
  return <section className="inspector-section candidate-review"><div className="section-title"><span>Candidate review</span><span className="mono-value">{reviewable.length}/5 current</span></div>{reviewable.length === 0 ? <p className="capability-note">No current candidate take is available. A verified adapter must generate one before review.</p> : reviewable.slice(0, 5).map((candidate) => { const evaluation = evaluations[candidate.id]; const accepted = segment.accepted_candidate_id === candidate.id; return <article className="candidate-card" key={candidate.id}><div className="candidate-heading"><strong>{accepted ? "Accepted take" : "Candidate take"}</strong><span>r{candidate.revision}</span></div><span className="candidate-model">{candidate.model_id}</span><audio controls preload="metadata" src={assetUrl(project.id, candidate.audio_asset_id)} /><div className="candidate-actions"><button className="outline-button" disabled={busy} onClick={() => onReview(candidate, "evaluate")} type="button">Evaluate</button><button className="outline-button" disabled={busy || accepted} onClick={() => onReview(candidate, "accept")} type="button">{accepted ? "Accepted" : "Accept"}</button></div>{evaluation ? <div className="candidate-metrics">{evaluation.metrics.slice(0, 3).map((metric) => <span key={metric.metric_id}>{metric.metric_id.split(".").at(-1)}: {metric.status === "ok" ? metric.value?.toFixed(3) : metric.status}</span>)}<a href={evaluation.report_markdown_url} rel="noreferrer" target="_blank">Report</a></div> : null}</article>; })}</section>;
}

function IconButton({ children, label, onClick }: { children: ReactNode; label: string; onClick?: () => void }) {
  return <button className="icon-button" aria-label={label} onClick={onClick} title={label}>{children}</button>;
}

function PanelHeading({ icon, title }: { icon: ReactNode; title: string }) {
  return <h2 className="panel-heading">{icon}<span>{title}</span></h2>;
}

function Resource({ active = false, detail, icon, label }: { active?: boolean; detail: string; icon: ReactNode; label: string }) {
  return <span className={`resource ${active ? "active" : ""}`}><span className="resource-icon">{icon}</span><span><strong>{label}</strong><small>{detail}</small></span></span>;
}

function Timeline({ acceptedCandidateCount, currentCandidateCount, maximumEndUs, onSelect, project, selectedSegmentId }: { acceptedCandidateCount: number; currentCandidateCount: number; maximumEndUs: number; onSelect: (id: string) => void; project: Project; selectedSegmentId: string | null }) {
  const marks = Array.from({ length: 6 }, (_, index) => formatSeconds((maximumEndUs * index) / 5));
  return <section className="timeline" aria-label="Dubbing timeline"><div className="timeline-header"><span>Timeline</span><span className="mono-value">{project.segments.length} local cues</span></div><div className="ruler">{marks.map((mark) => <span key={mark}>{mark}</span>)}</div><div className="track original-track"><span className="track-label">Original</span><div className="waveform original-wave" /></div><div className="track dialogue-track"><span className="track-label">Dialogue</span><div className="segment-lane">{project.segments.map((segment) => <button className={`segment-block ${segment.id === selectedSegmentId ? "selected" : ""}`} key={segment.id} onClick={() => onSelect(segment.id)} style={{ left: `${(segment.range.start_us / maximumEndUs) * 100}%`, width: `${Math.max(8, ((segment.range.end_us - segment.range.start_us) / maximumEndUs) * 100)}%` }} title={segment.text}><span>{segment.text}</span><small>{formatRange(segment)}</small></button>)}</div></div><div className="track candidate-track"><span className="track-label">Candidate</span><div className="empty-track">{acceptedCandidateCount ? `${acceptedCandidateCount} accepted candidate take${acceptedCandidateCount === 1 ? "" : "s"} ready for local export.` : currentCandidateCount ? `${currentCandidateCount} current candidate take${currentCandidateCount === 1 ? "" : "s"} ready for review.` : "A verified adapter is required before candidate generation."}</div></div></section>;
}

function formatSeconds(microseconds: number): string {
  return `${(microseconds / 1_000_000).toFixed(2)}s`;
}

function formatRange(segment: DubbingSegment): string {
  return `${formatSeconds(segment.range.start_us)} - ${formatSeconds(segment.range.end_us)}`;
}
