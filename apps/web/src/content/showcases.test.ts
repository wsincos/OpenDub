import { describe, expect, it } from "vitest";

import { getShowcaseCase, publicShowcaseUrl, showcaseCases } from "./showcases";

describe("showcase content", () => {
  it("exposes Case 03 and the authorized Case 04 with their declared source mappings", () => {
    const case03 = getShowcaseCase("case-03");
    const case04 = getShowcaseCase("case-04");

    expect(showcaseCases).toHaveLength(4);
    expect(case03).toMatchObject({
      displayName: "Animated cinematic scene",
      contentStatus: "archived_research_example",
      timelineEligible: false,
      mediaRelease: "v3",
      durationSeconds: 1.56,
    });
    expect(showcaseCases.map((item) => item.durationSeconds)).toEqual([3, 1.36, 1.56, 7.8]);
    expect(case03?.artifacts.map((artifact) => [artifact.path, artifact.methodId])).toEqual([
      ["gt.mp4", undefined],
      ["hpmdubbing.mp4", "galaxycong/hpmdubbing"],
      ["styledubber.mp4", "galaxycong/styledubber"],
      ["emodubber.mp4", "galaxycong/emodubber"],
    ]);
    expect(case03?.artifacts[0]?.sha256).toBe("eb6406fb6b84f46eb789439c8c4da246beab1f5410bb92f73b08f3352f4d61e2");
    expect(publicShowcaseUrl(case03!, "hpmdubbing.mp4")).toBe("/showcases/v3/case-03/hpmdubbing.mp4");
    expect(case03?.artifacts[1]?.featureUrl).toBe("/showcases/v3/case-03/features/hpmdubbing.json");
    expect(case04).toMatchObject({
      displayName: "Presenter and display scene",
      contentStatus: "archived_research_example",
      timelineEligible: false,
      mediaRelease: "v4",
      durationSeconds: 7.8,
    });
    expect(case04?.artifacts.map((artifact) => [artifact.path, artifact.methodId])).toEqual([
      ["gt.mp4", undefined],
      ["hpmdubbing.mp4", "galaxycong/hpmdubbing"],
      ["styledubber.mp4", "galaxycong/styledubber"],
      ["emodubber.mp4", "galaxycong/emodubber"],
    ]);
    expect(publicShowcaseUrl(case04!, "emodubber.mp4")).toBe("/showcases/v4/case-04/emodubber.mp4");
  });
});
