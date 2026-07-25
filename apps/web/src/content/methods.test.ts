import { expect, test } from "vitest";

import { methods } from "./methods";

test("derives the three method summaries from their fixed source manifests", () => {
  expect(methods.map((method) => method.title)).toEqual(["HPMDubbing", "StyleDubber", "EmoDubber"]);
  expect(methods.map((method) => method.sourceCommit)).toEqual([
    "f50dfa7df649208c674f151e52ad0a38d0b0bd43",
    "bc431c8f67e885433c5c23163a8eaccb0dd41175",
    "553fa054160fed17e757125d185e5a61ef6ed437",
  ]);
  expect(methods.every((method) => method.sourceUrl.endsWith(`/tree/${method.sourceCommit}`))).toBe(true);
  expect(methods.every((method) => method.status === "CONCEPT")).toBe(true);
});
