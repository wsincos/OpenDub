import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { StudioApp } from "./StudioApp";

const emptyProject = {
  id: "019ce522-9f44-7e5e-b6c8-d26033e40f22",
  name: "Emotion-directed scene",
  revision: 1,
  created_at: "2026-07-26T00:00:00Z",
  updated_at: "2026-07-26T00:00:00Z",
  assets: [],
  voice_references: [],
  input_authorizations: [],
  method_selection: null,
  segments: [],
  candidates: [],
  consents: [],
};

function jsonResponse(payload: unknown): Response {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("StudioApp", () => {
  it("persists an Atlas-selected complete method when it creates the local project", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(jsonResponse(emptyProject))
      .mockResolvedValueOnce(jsonResponse({
        ...emptyProject,
        revision: 2,
        method_selection: {
          method_id: "galaxycong/emodubber",
          method_manifest_version: "method-manifest@553fa054160fed17e757125d185e5a61ef6ed437",
          declared_need: "Use explicit emotion category and intensity as part of the complete dubbing method.",
          required_inputs: ["Video", "Target text", "Authorized reference speech"],
          optional_controls: ["Emotion category", "Emotion intensity"],
          runtime_status: "unavailable",
          content_modes: ["concept"],
          evidence_revision: "553fa054160fed17e757125d185e5a61ef6ed437",
          selected_at: "2026-07-26T00:00:00Z",
        },
      }));
    vi.stubGlobal("fetch", fetchMock);

    render(<MemoryRouter initialEntries={["/studio?method=emodubber"]}><StudioApp /></MemoryRouter>);

    expect(screen.getByText("OPEN DUB / LOCAL PROJECT DESK")).toBeVisible();
    expect(screen.getByText("NEW LOCAL PROJECT")).toBeVisible();
    await user.type(screen.getByLabelText("Project name"), "Emotion-directed scene");
    await user.click(screen.getByRole("button", { name: "Create local project" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    const [url, request] = fetchMock.mock.calls[2] as [string, RequestInit];
    expect(url).toBe("http://127.0.0.1:8000/api/v1/projects/019ce522-9f44-7e5e-b6c8-d26033e40f22/method-selection");
    expect(JSON.parse(String(request.body))).toMatchObject({
      method_id: "galaxycong/emodubber",
      optional_controls: ["Emotion category", "Emotion intensity"],
      expected_revision: 1,
    });
  });
});
