import animationManifest from "../../../../content/showcases/v2/animation-1.json";
import humanManifest from "../../../../content/showcases/v2/human-0.json";
import case03Manifest from "../../../../content/showcases/v3/case-03.json";
import case04Manifest from "../../../../content/showcases/v4/case-04.json";

export type ShowcaseStatus = "archived_research_example" | "replay" | "blocked";
export type ShowcaseMethodId = "galaxycong/hpmdubbing" | "galaxycong/styledubber" | "galaxycong/emodubber";

export type ShowcaseArtifact = {
  featureUrl: string;
  melUrl: string;
  contactFrameUrls: string[];
  role: "ground_truth" | "method_output";
  label: string;
  path: string;
  sha256: string;
  methodId?: ShowcaseMethodId;
};

export type ShowcaseCase = {
  id: string;
  displayName: string;
  durationSeconds: number;
  mediaRelease: "v2" | "v3" | "v4";
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
  sha256: string;
  method_id?: ShowcaseMethodId;
};

type ShowcaseManifest = {
  case_id: string;
  display_name: string;
  visual_type: ShowcaseCase["visualType"];
  duration_seconds: number;
  content_status: ShowcaseStatus;
  timeline_eligible: boolean;
  rights: { redistribution: string };
  artifacts: ManifestArtifact[];
};

type VersionedShowcaseManifest = {
  manifest: ShowcaseManifest;
  mediaRelease: ShowcaseCase["mediaRelease"];
};

const manifests: VersionedShowcaseManifest[] = [
  { manifest: humanManifest as ShowcaseManifest, mediaRelease: "v2" },
  { manifest: animationManifest as ShowcaseManifest, mediaRelease: "v2" },
  { manifest: case03Manifest as ShowcaseManifest, mediaRelease: "v3" },
  { manifest: case04Manifest as ShowcaseManifest, mediaRelease: "v4" },
];

export const showcaseCases = manifests.map(({ manifest, mediaRelease }) => toShowcaseCase(manifest, mediaRelease));

export function getShowcaseCase(caseId: string): ShowcaseCase | undefined {
  return showcaseCases.find((showcase) => showcase.id === caseId);
}

export function publicShowcaseUrl(caseItem: ShowcaseCase, path: string): string {
  return `/showcases/${caseItem.mediaRelease}/${caseItem.id}/${path}`;
}

function toShowcaseCase(manifest: ShowcaseManifest, mediaRelease: ShowcaseCase["mediaRelease"]): ShowcaseCase {
  if (manifest.rights.redistribution !== "allowed-for-opendub-v2") {
    throw new Error(`Showcase ${manifest.case_id} cannot be rendered without redistribution permission.`);
  }
  if (manifest.content_status === "replay" && !manifest.timeline_eligible) {
    throw new Error(`Replay showcase ${manifest.case_id} must have an eligible timeline contract.`);
  }
  return {
    id: manifest.case_id,
    displayName: manifest.display_name,
    durationSeconds: manifest.duration_seconds,
    mediaRelease,
    visualType: manifest.visual_type,
    contentStatus: manifest.content_status,
    timelineEligible: manifest.timeline_eligible,
    artifacts: manifest.artifacts.map((artifact) => ({
      role: artifact.role,
      label: artifact.role === "ground_truth" ? "Reference performance" : artifact.label,
      path: artifact.path,
      sha256: artifact.sha256,
      methodId: artifact.method_id,
      featureUrl: `/showcases/${mediaRelease}/${manifest.case_id}/features/${artifact.path.replace(/\.mp4$/, "")}.json`,
      melUrl: `/showcases/${mediaRelease}/${manifest.case_id}/features/${artifact.path.replace(/\.mp4$/, "")}.mel.png`,
      contactFrameUrls: Array.from({ length: 5 }, (_, index) => `/showcases/${mediaRelease}/${manifest.case_id}/contacts/${artifact.path.replace(/\.mp4$/, "")}-${index}.jpg`),
    })),
    posterUrl: `/showcases/${mediaRelease}/${manifest.case_id}/poster.jpg`,
  };
}
