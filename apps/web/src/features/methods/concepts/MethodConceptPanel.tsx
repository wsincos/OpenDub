import { HpmHierarchyView } from "./HpmHierarchyView";
import { EmoGuidanceView } from "./EmoGuidanceView";
import { StyleScaleView } from "./StyleScaleView";

export function MethodConceptPanel({ methodSlug }: { methodSlug: string }) {
  if (methodSlug === "hpmdubbing") return <HpmHierarchyView />;
  if (methodSlug === "styledubber") return <StyleScaleView />;
  if (methodSlug === "emodubber") return <EmoGuidanceView />;
  return null;
}
