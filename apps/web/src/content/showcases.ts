import animationManifest from "../../../../content/showcases/v2/animation-1.json";
import humanManifest from "../../../../content/showcases/v2/human-0.json";

export type ShowcaseStatus = "archived_research_example" | "replay" | "blocked";
export type ShowcaseMethodId = "galaxycong/hpmdubbing" | "galaxycong/styledubber" | "galaxycong/emodubber";

export type ShowcaseArtifact = {
  role: "ground_truth" | "method_output";
  label: string;
  path: string;
  methodId?: ShowcaseMethodId;
};

export type ShowcaseCase = {
  id: string;
  displayName: string;
  visualType: "human" | "animation";
  contentStatus: ShowcaseStatus;
  timelineEligible: boolean;
  artifacts: ShowcaseArtifact[];
  posterUrl: string;
};

type ManifestArtifact = {
  role: ShowcaseArtifact["role"];
  label: string;
  path: string;
  method_id?: ShowcaseMethodId;
};

type ShowcaseManifest = {
  case_id: string;
  display_name: string;
  visual_type: ShowcaseCase["visualType"];
  content_status: ShowcaseStatus;
  timeline_eligible: boolean;
  rights: { redistribution: string };
  artifacts: ManifestArtifact[];
};

const manifests = [humanManifest, animationManifest] as ShowcaseManifest[];

export const showcaseCases = manifests.map(toShowcaseCase);

export function getShowcaseCase(caseId: string): ShowcaseCase | undefined {
  return showcaseCases.find((showcase) => showcase.id === caseId);
}

export function publicShowcaseUrl(caseId: string, path: string): string {
  return `/showcases/v2/${caseId}/${path}`;
}

function toShowcaseCase(manifest: ShowcaseManifest): ShowcaseCase {
  if (manifest.rights.redistribution !== "allowed-for-opendub-v2") {
    throw new Error(`Showcase ${manifest.case_id} cannot be rendered without redistribution permission.`);
  }
  if (manifest.content_status === "replay" && !manifest.timeline_eligible) {
    throw new Error(`Replay showcase ${manifest.case_id} must have an eligible timeline contract.`);
  }
  return {
    id: manifest.case_id,
    displayName: manifest.display_name,
    visualType: manifest.visual_type,
    contentStatus: manifest.content_status,
    timelineEligible: manifest.timeline_eligible,
    artifacts: manifest.artifacts.map((artifact) => ({
      role: artifact.role,
      label: artifact.label,
      path: artifact.path,
      methodId: artifact.method_id,
    })),
    posterUrl: publicShowcaseUrl(manifest.case_id, "poster.jpg"),
  };
}
