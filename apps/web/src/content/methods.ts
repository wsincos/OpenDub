import emoManifest from "../../../../content/methods/emodubber/method.json";
import hpmManifest from "../../../../content/methods/hpmdubbing/method.json";
import styleManifest from "../../../../content/methods/styledubber/method.json";

export type MethodNode = {
  id: string;
  label: string;
  short: string;
  detail: string;
  tone: "video" | "text" | "voice" | "prosody" | "style" | "emotion" | "output";
  signals: string[];
};

export type MethodDefinition = {
  slug: "hpmdubbing" | "styledubber" | "emodubber";
  id: "galaxycong/hpmdubbing" | "galaxycong/styledubber" | "galaxycong/emodubber";
  title: "HPMDubbing" | "StyleDubber" | "EmoDubber";
  venue: string;
  year: number;
  question: string;
  contribution: string;
  status: "CONCEPT" | "REPLAY" | "LIVE";
  color: string;
  paperUrl: string;
  sourceUrl: string;
  sourceCommit: string;
  path: string[];
  nodes: MethodNode[];
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

type MethodManifestFile = {
  id: MethodDefinition["id"];
  slug: MethodDefinition["slug"];
  short_title: MethodDefinition["title"];
  conference: string;
  year: number;
  question: { en: string };
  contribution: { en: string };
  content_modes: string[];
  paper: { url: string };
  source: { repository: string; commit: string };
  graph: { nodes: ManifestNode[]; overview_path: string[] };
  signals: ManifestSignal[];
};

const presentation: Record<MethodDefinition["id"], { color: string; canvasNodeIds: string[] }> = {
  "galaxycong/hpmdubbing": {
    color: "#1877c9",
    canvasNodeIds: ["lip_duration", "face_affect", "scene_emotion", "hierarchical_prosody", "mel_decoder", "vocoder"],
  },
  "galaxycong/styledubber": {
    color: "#7656c1",
    canvasNodeIds: ["phoneme_view", "mpa", "pla", "usl", "mel_decoder", "refinement"],
  },
  "galaxycong/emodubber": {
    color: "#c84b61",
    canvasNodeIds: ["lpa", "pe", "speaker_identity", "emotion_control", "fuec", "pngm"],
  },
};

const manifests = [hpmManifest, styleManifest, emoManifest] as unknown as MethodManifestFile[];

export const methods = manifests.map(toMethod);

export function getMethod(slug: string | undefined): MethodDefinition | undefined {
  return methods.find((method) => method.slug === slug);
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
    question: manifest.question.en,
    contribution: manifest.contribution.en,
    status: deriveContentStatus(manifest.content_modes),
    color: config.color,
    paperUrl: manifest.paper.url,
    sourceUrl: `${manifest.source.repository}/tree/${manifest.source.commit}`,
    sourceCommit: manifest.source.commit,
    path: manifest.graph.overview_path,
    nodes: config.canvasNodeIds.map((nodeId) => {
      const node = nodesById.get(nodeId);
      if (!node) throw new Error(`Atlas manifest ${manifest.id} is missing canvas node ${nodeId}`);
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
