export type AssetKind = "video" | "audio" | "image" | "subtitle" | "document";
export type MaterialSource = "self_recorded" | "licensed" | "public_domain" | "authorized_other";
export type EmotionLabel = "neutral" | "happy" | "sad" | "angry" | "fearful" | "surprised" | "custom";

export type ProjectSummary = {
  id: string;
  name: string;
  revision: number;
  updated_at: string;
};

export type MediaAsset = {
  id: string;
  kind: AssetKind;
  display_name: string;
  relative_path: string;
  sha256: string;
  size_bytes: number;
  duration_us: number | null;
};

export type VoiceReference = {
  id: string;
  asset_id: string;
  consent_id: string;
  speaker_label: string;
};

export type DubbingSegment = {
  id: string;
  range: { start_us: number; end_us: number };
  text: string;
  language: string;
  character_id: string;
  voice_reference_id: string;
  emotion: { label: EmotionLabel; intensity: number };
  adapter_id: string;
  status: string;
  accepted_candidate_id: string | null;
  revision: number;
};

export type DubbingCandidate = {
  id: string;
  segment_id: string;
  segment_revision: number;
  audio_asset_id: string;
  adapter_id: string;
  model_id: string;
  seed: number;
  revision: number;
};

export type CandidateEvaluation = {
  candidate_id: string;
  metrics: Array<{
    metric_id: string;
    version: string;
    status: "ok" | "not_applicable" | "unavailable" | "failed";
    value: number | null;
    unit: string | null;
  }>;
  report_json_url: string;
  report_markdown_url: string;
};

export type Project = ProjectSummary & {
  assets: MediaAsset[];
  voice_references: VoiceReference[];
  segments: DubbingSegment[];
  candidates: DubbingCandidate[];
  consents: unknown[];
};

type AssetMutation = MediaAsset & { project_revision: number };
type VoiceReferenceMutation = VoiceReference & { project_revision: number };
type SegmentMutation = DubbingSegment & { project_revision: number };
type RenderMutation = {
  project_id: string;
  project_revision: number;
  mix_mode: "preserve" | "duck" | "remove";
  sample_rate: number;
  dubbing_audio_url: string;
  dubbed_video_url: string | null;
  manifest_url: string;
};

const apiBase = import.meta.env.VITE_OPENDUB_API_BASE ?? "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, options);
  if (response.ok) return response.json() as Promise<T>;
  const body = (await response.json().catch(() => null)) as { detail?: { message?: string } } | null;
  throw new Error(body?.detail?.message ?? `Local API returned ${response.status}`);
}

export function listProjects(): Promise<ProjectSummary[]> {
  return request<ProjectSummary[]>("/api/v1/projects");
}

export function getProject(projectId: string): Promise<Project> {
  return request<Project>(`/api/v1/projects/${projectId}`);
}

export function createProject(name: string): Promise<Project> {
  return request<Project>("/api/v1/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
}

export function assetUrl(projectId: string, assetId: string): string {
  return `${apiBase}/api/v1/projects/${projectId}/assets/${assetId}`;
}

export async function uploadAsset(
  projectId: string,
  file: File,
  kind: AssetKind,
  expectedRevision: number,
): Promise<AssetMutation> {
  if (file.size > 24 * 1024 * 1024) throw new Error("Use a file smaller than 24 MB in this local Studio build.");
  return request<AssetMutation>(`/api/v1/projects/${projectId}/assets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      kind,
      filename: file.name,
      content_base64: await fileToBase64(file),
      expected_revision: expectedRevision,
    }),
  });
}

export function createVoiceReference(
  projectId: string,
  input: { assetId: string; speakerLabel: string; materialSource: MaterialSource; allowGeneratedOutputDistribution: boolean; expectedRevision: number },
): Promise<VoiceReferenceMutation> {
  return request<VoiceReferenceMutation>(`/api/v1/projects/${projectId}/voice-references`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      asset_id: input.assetId,
      speaker_label: input.speakerLabel,
      material_source: input.materialSource,
      allow_generated_output_distribution: input.allowGeneratedOutputDistribution,
      expected_revision: input.expectedRevision,
    }),
  });
}

export function createSegment(
  projectId: string,
  input: {
    startUs: number;
    endUs: number;
    text: string;
    language: string;
    voiceReferenceId: string;
    adapterId: string;
    emotionLabel: EmotionLabel;
    emotionIntensity: number;
    expectedRevision: number;
  },
): Promise<SegmentMutation> {
  return request<SegmentMutation>(`/api/v1/projects/${projectId}/segments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      start_us: input.startUs,
      end_us: input.endUs,
      text: input.text,
      language: input.language,
      voice_reference_id: input.voiceReferenceId,
      adapter_id: input.adapterId,
      emotion_label: input.emotionLabel,
      emotion_intensity: input.emotionIntensity,
      expected_revision: input.expectedRevision,
    }),
  });
}

export function updateSegment(
  projectId: string,
  segmentId: string,
  input: {
    text: string;
    startUs: number;
    endUs: number;
    language: string;
    voiceReferenceId: string;
    emotionLabel: EmotionLabel;
    emotionIntensity: number;
    expectedRevision: number;
  },
): Promise<SegmentMutation> {
  return request<SegmentMutation>(`/api/v1/projects/${projectId}/segments/${segmentId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: input.text,
      start_us: input.startUs,
      end_us: input.endUs,
      language: input.language,
      voice_reference_id: input.voiceReferenceId,
      emotion_label: input.emotionLabel,
      emotion_intensity: input.emotionIntensity,
      expected_revision: input.expectedRevision,
    }),
  });
}

export function importSubtitleSegments(
  projectId: string,
  input: {
    assetId: string;
    language: string;
    voiceReferenceId: string;
    adapterId: string;
    expectedRevision: number;
  },
): Promise<Project> {
  return request<Project>(`/api/v1/projects/${projectId}/segments/import-subtitles`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      asset_id: input.assetId,
      language: input.language,
      voice_reference_id: input.voiceReferenceId,
      adapter_id: input.adapterId,
      expected_revision: input.expectedRevision,
    }),
  });
}

export function deleteSegment(projectId: string, segmentId: string, expectedRevision: number): Promise<Project> {
  return request<Project>(`/api/v1/projects/${projectId}/segments/${segmentId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expected_revision: expectedRevision }),
  });
}

export function acceptCandidate(
  projectId: string,
  segmentId: string,
  candidateId: string,
  expectedRevision: number,
): Promise<Project> {
  return request<Project>(
    `/api/v1/projects/${projectId}/segments/${segmentId}/candidates/${candidateId}/accept`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expected_revision: expectedRevision }),
    },
  );
}

export async function evaluateCandidate(projectId: string, candidateId: string): Promise<CandidateEvaluation> {
  const result = await request<CandidateEvaluation>(
    `/api/v1/projects/${projectId}/candidates/${candidateId}/evaluate`,
    { method: "POST" },
  );
  return {
    ...result,
    report_json_url: `${apiBase}${result.report_json_url}`,
    report_markdown_url: `${apiBase}${result.report_markdown_url}`,
  };
}

export async function renderAcceptedCandidates(projectId: string): Promise<RenderMutation> {
  const result = await request<RenderMutation>(`/api/v1/projects/${projectId}/renders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mix_mode: "remove" }),
  });
  return {
    ...result,
    dubbing_audio_url: `${apiBase}${result.dubbing_audio_url}`,
    dubbed_video_url: result.dubbed_video_url ? `${apiBase}${result.dubbed_video_url}` : null,
    manifest_url: `${apiBase}${result.manifest_url}`,
  };
}

async function fileToBase64(file: File): Promise<string> {
  const bytes = new Uint8Array(await file.arrayBuffer());
  const chunks: string[] = [];
  const chunkSize = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunkSize) {
    chunks.push(String.fromCharCode(...bytes.subarray(offset, offset + chunkSize)));
  }
  return btoa(chunks.join(""));
}
