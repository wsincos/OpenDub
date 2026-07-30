import emoManifest from "../../content/methods/emodubber/method.json";
import hpmManifest from "../../content/methods/hpmdubbing/method.json";
import styleManifest from "../../content/methods/styledubber/method.json";

import type { MethodSelectionDraft } from "../api/client";

export type MethodNode = {
  id: string;
  label: string;
  short: string;
  detail: string;
  tone: "video" | "text" | "voice" | "prosody" | "style" | "emotion" | "output";
  signals: string[];
};

export type MethodEdge = {
  id: string;
  source: string;
  target: string;
};

export type GraphPosition = {
  x: number;
  y: number;
};

export type MethodDefinition = {
  slug: "hpmdubbing" | "styledubber" | "emodubber";
  id: "galaxycong/hpmdubbing" | "galaxycong/styledubber" | "galaxycong/emodubber";
  title: "HPMDubbing" | "StyleDubber" | "EmoDubber";
  venue: string;
  year: number;
  teamLabel: "TEAM-DEVELOPED COMPLETE METHOD";
  originalFocus: string;
  publishedRecord: { title: string; venue: string; year: number };
  question: string;
  contribution: string;
  status: "CONCEPT" | "REPLAY" | "LIVE";
  color: string;
  paperUrl: string;
  sourceUrl: string;
  sourceCommit: string;
  sourceLicense: string;
  runtimeStatus: "unavailable" | "experimental" | "stable";
  path: string[];
  nodes: MethodNode[];
  edges: MethodEdge[];
  positions: Record<string, GraphPosition>;
  overviewNodeIds: string[];
};

type ManifestNode = {
  id: string;
  label: { en: string };
  short_label: string;
  kind: string;
  summary: { en: string };
  visualization_slots: string[];
};

type ManifestSignal = { id: string; label: { en: string } };
type ManifestEdge = { id: string; source: string; target: string };

type MethodManifestFile = {
  id: MethodDefinition["id"];
  slug: MethodDefinition["slug"];
  short_title: MethodDefinition["title"];
  conference: string;
  year: number;
  question: { en: string };
  contribution: { en: string };
  content_modes: string[];
  paper: { title: string; url: string };
  source: { repository: string; commit: string; license: string };
  runtime_status: MethodDefinition["runtimeStatus"];
  graph: { nodes: ManifestNode[]; edges: ManifestEdge[]; overview_path: string[] };
  signals: ManifestSignal[];
};

const presentation: Record<MethodDefinition["id"], { color: string; originalFocus: string; overviewNodeIds: string[]; positions: Record<string, GraphPosition> }> = {
  "galaxycong/hpmdubbing": {
    color: "#1877c9",
    originalFocus: "Visual prosody across lip, face, and scene cues.",
    overviewNodeIds: ["lip_duration", "face_affect", "scene_emotion", "hierarchical_prosody", "mel_decoder", "vocoder"],
    positions: {
      video: { x: 9, y: 22 }, text: { x: 9, y: 50 }, reference_speech: { x: 9, y: 78 },
      lip_duration: { x: 29, y: 22 }, face_affect: { x: 29, y: 50 }, scene_emotion: { x: 29, y: 78 },
      hierarchical_prosody: { x: 52, y: 50 }, mel_decoder: { x: 70, y: 50 }, vocoder: { x: 84, y: 50 }, dubbed_speech: { x: 96, y: 50 },
    },
  },
  "galaxycong/styledubber": {
    color: "#7656c1",
    originalFocus: "Local pronunciation and global character style.",
    overviewNodeIds: ["phoneme_view", "mpa", "pla", "usl", "mel_decoder", "refinement"],
    positions: {
      video: { x: 9, y: 22 }, text: { x: 9, y: 50 }, reference_speech: { x: 9, y: 78 },
      phoneme_view: { x: 27, y: 50 }, mpa: { x: 46, y: 30 }, pla: { x: 46, y: 70 },
      usl: { x: 64, y: 50 }, mel_decoder: { x: 78, y: 50 }, refinement: { x: 89, y: 50 }, dubbed_speech: { x: 97, y: 50 },
    },
  },
  "galaxycong/emodubber": {
    color: "#c84b61",
    originalFocus: "Alignment, pronunciation, identity, and directed emotion.",
    overviewNodeIds: ["lpa", "pe", "speaker_identity", "emotion_control", "fuec", "pngm"],
    positions: {
      video: { x: 9, y: 23 }, text: { x: 9, y: 51 }, reference_speech: { x: 9, y: 79 },
      lpa: { x: 28, y: 32 }, pe: { x: 43, y: 48 }, speaker_identity: { x: 59, y: 64 },
      emotion_control: { x: 59, y: 27 }, fuec: { x: 75, y: 48 }, pngm: { x: 87, y: 48 }, dubbed_speech: { x: 97, y: 48 },
    },
  },
};

const manifests = [hpmManifest, styleManifest, emoManifest] as unknown as MethodManifestFile[];

export const methods = manifests.map(toMethod);

export function getMethod(slug: string | undefined): MethodDefinition | undefined {
  return methods.find((method) => method.slug === slug);
}

export function getMethodById(id: MethodDefinition["id"] | undefined): MethodDefinition | undefined {
  return methods.find((method) => method.id === id);
}

export function englishIndefiniteArticle(label: string): "a" | "an" {
  return /^(?:[aeiou]|hpm)/i.test(label) ? "an" : "a";
}

const methodSelectionMetadata: Record<MethodDefinition["id"], Pick<MethodSelectionDraft, "declaredNeed" | "optionalControls">> = {
  "galaxycong/hpmdubbing": {
    declaredNeed: "Understand how hierarchical Lip, Face, and Scene cues shape dubbing prosody.",
    optionalControls: [],
  },
  "galaxycong/styledubber": {
    declaredNeed: "Inspect phoneme- and utterance-level speaking style at multiple temporal scales.",
    optionalControls: [],
  },
  "galaxycong/emodubber": {
    declaredNeed: "Use explicit emotion category and intensity as part of the complete dubbing method.",
    optionalControls: ["Emotion category", "Emotion intensity"],
  },
};

export function createMethodSelectionDraft(method: MethodDefinition): MethodSelectionDraft {
  const metadata = methodSelectionMetadata[method.id];
  return {
    methodId: method.id,
    methodManifestVersion: `method-manifest@${method.sourceCommit}`,
    declaredNeed: metadata.declaredNeed,
    requiredInputs: ["Video", "Target text", "Authorized reference speech"],
    optionalControls: metadata.optionalControls,
    runtimeStatus: method.runtimeStatus,
    contentModes: [method.status.toLowerCase() as MethodSelectionDraft["contentModes"][number]],
    evidenceRevision: method.sourceCommit,
  };
}

function toMethod(manifest: MethodManifestFile): MethodDefinition {
  const config = presentation[manifest.id];
  const nodesById = new Map(manifest.graph.nodes.map((node) => [node.id, node]));
  const signalsById = new Map(manifest.signals.map((signal) => [signal.id, signal]));

  return {
    slug: manifest.slug,
    id: manifest.id,
    title: manifest.short_title,
    venue: manifest.conference,
    year: manifest.year,
    teamLabel: "TEAM-DEVELOPED COMPLETE METHOD",
    originalFocus: config.originalFocus,
    publishedRecord: { title: manifest.paper.title, venue: manifest.conference, year: manifest.year },
    question: manifest.question.en,
    contribution: manifest.contribution.en,
    status: deriveContentStatus(manifest.content_modes),
    color: config.color,
    paperUrl: manifest.paper.url,
    sourceUrl: `${manifest.source.repository}/tree/${manifest.source.commit}`,
    sourceCommit: manifest.source.commit,
    sourceLicense: manifest.source.license,
    runtimeStatus: manifest.runtime_status,
    path: manifest.graph.overview_path,
    overviewNodeIds: config.overviewNodeIds,
    positions: config.positions,
    edges: manifest.graph.edges.map((edge) => ({ ...edge })),
    nodes: manifest.graph.nodes.map((node) => {
      if (!config.positions[node.id]) throw new Error(`Atlas presentation ${manifest.id} is missing a position for ${node.id}`);
      return {
        id: node.id,
        label: node.label.en,
        short: node.short_label,
        detail: node.summary.en,
        tone: nodeTone(node.kind),
        signals: node.visualization_slots.map((signalId) => signalsById.get(signalId)?.label.en ?? signalId),
      };
    }),
  };
}

function deriveContentStatus(contentModes: string[]): MethodDefinition["status"] {
  if (contentModes.includes("live")) return "LIVE";
  if (contentModes.includes("replay")) return "REPLAY";
  return "CONCEPT";
}

function nodeTone(kind: string): MethodNode["tone"] {
  if (kind === "text") return "text";
  if (kind === "voice") return "voice";
  if (kind === "style") return "style";
  if (kind === "emotion") return "emotion";
  if (kind === "prosody" || kind === "acoustic") return "prosody";
  if (kind === "generation" || kind === "output") return "output";
  return "video";
}
