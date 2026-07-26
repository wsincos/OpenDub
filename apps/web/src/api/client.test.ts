import { afterEach, describe, expect, it, vi } from "vitest";

import { exportProjectPreparation } from "./client";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("exportProjectPreparation", () => {
  it("requests a local preparation record and returns its local manifest URL", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      project_id: "019ce522-9f44-7e5e-b6c8-d26033e40f22",
      project_revision: 4,
      manifest_url: "/api/v1/projects/019ce522-9f44-7e5e-b6c8-d26033e40f22/preparation-exports/revision-4/preparation.json",
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);

    const exported = await exportProjectPreparation("019ce522-9f44-7e5e-b6c8-d26033e40f22");

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/api/v1/projects/019ce522-9f44-7e5e-b6c8-d26033e40f22/preparation-export",
      { method: "POST" },
    );
    expect(exported.manifest_url).toBe(
      "http://127.0.0.1:8000/api/v1/projects/019ce522-9f44-7e5e-b6c8-d26033e40f22/preparation-exports/revision-4/preparation.json",
    );
  });
});
