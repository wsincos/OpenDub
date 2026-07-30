import { expect, test } from "vitest";

import { createMethodSelectionDraft, englishIndefiniteArticle, getMethod, methods } from "./methods";

test("derives the three method summaries from their fixed source manifests", () => {
  expect(methods.map((method) => method.title)).toEqual(["HPMDubbing", "StyleDubber", "EmoDubber"]);
  expect(methods.map((method) => method.sourceCommit)).toEqual([
    "f50dfa7df649208c674f151e52ad0a38d0b0bd43",
    "bc431c8f67e885433c5c23163a8eaccb0dd41175",
    "553fa054160fed17e757125d185e5a61ef6ed437",
  ]);
  expect(methods.every((method) => method.sourceUrl.endsWith(`/tree/${method.sourceCommit}`))).toBe(true);
  expect(methods.every((method) => method.status === "CONCEPT")).toBe(true);
  expect(methods.every((method) => method.teamLabel === "TEAM-DEVELOPED COMPLETE METHOD")).toBe(true);
  expect(methods.map((method) => method.originalFocus)).toEqual([
    "Visual prosody across lip, face, and scene cues.",
    "Local pronunciation and global character style.",
    "Alignment, pronunciation, identity, and directed emotion.",
  ]);
  expect(methods.every((method) => method.publishedRecord.title.length > 0)).toBe(true);
});

test("creates an evidence-bound selection draft without inventing shared controls", () => {
  const selection = createMethodSelectionDraft(getMethod("emodubber")!);

  expect(selection.methodId).toBe("galaxycong/emodubber");
  expect(selection.requiredInputs).toEqual([
    "Video",
    "Target text",
    "Authorized reference speech",
  ]);
  expect(selection.optionalControls).toEqual(["Emotion category", "Emotion intensity"]);
  expect(selection.contentModes).toEqual(["concept"]);
  expect(selection.runtimeStatus).toBe("unavailable");
});

test("uses a grammatically correct article when handing each method to Studio", () => {
  expect(methods.map((method) => englishIndefiniteArticle(method.title))).toEqual(["an", "a", "an"]);
});
