import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Project } from "../../api/client";
import { StudioShell } from "./StudioShell";

const selectedProject: Project = {
  id: "019ce522-9f44-7e5e-b6c8-d26033e40f22",
  name: "Emotion-directed scene",
  revision: 2,
  updated_at: "2026-07-26T00:00:00Z",
  assets: [],
  voice_references: [],
  input_authorizations: [],
  segments: [],
  candidates: [],
  consents: [],
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
};

const preparedProject: Project = {
  ...selectedProject,
  revision: 5,
  assets: [
    { id: "video-asset", kind: "video", display_name: "authorized-scene.mp4", relative_path: "assets/video.mp4", sha256: "a".repeat(64), size_bytes: 100, duration_us: 1_500_000 },
    { id: "voice-asset", kind: "audio", display_name: "authorized-reference.wav", relative_path: "assets/voice.wav", sha256: "b".repeat(64), size_bytes: 100, duration_us: 1_000_000 },
  ],
  voice_references: [{ id: "voice-reference", asset_id: "voice-asset", consent_id: "voice-consent", speaker_label: "Authorized performer" }],
  input_authorizations: [
    { id: "video-authorization", input_kind: "video", asset_id: "video-asset", content_sha256: "a".repeat(64), material_source: "self_recorded", authorization_purpose: "video_dubbing_project_preparation", accepted_at: "2026-07-26T00:00:00Z", revision: 1 },
    { id: "text-authorization", input_kind: "target_text", asset_id: null, content_sha256: "c".repeat(64), material_source: "self_recorded", authorization_purpose: "video_dubbing_project_preparation", accepted_at: "2026-07-26T00:00:00Z", revision: 1 },
  ],
  segments: [{ id: "segment", range: { start_us: 0, end_us: 1_200_000 }, text: "Authorized target line.", language: "en", character_id: "voice-reference", voice_reference_id: "voice-reference", emotion: { label: "happy", intensity: 0.7 }, adapter_id: "galaxycong/emodubber", status: "ready", accepted_candidate_id: null, revision: 1 }],
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("StudioShell", () => {
  it("makes the selected complete method and its evidence-bound runtime explicit", () => {
    render(
      <MemoryRouter>
        <StudioShell onBack={vi.fn()} onRefresh={vi.fn()} project={selectedProject} />
      </MemoryRouter>,
    );

    const configuration = screen.getByLabelText("Selected method configuration");
    expect(within(configuration).getByText("EmoDubber")).toBeVisible();
    expect(within(configuration).getByText("CONCEPT")).toBeVisible();
    expect(within(configuration).getByText("Video")).toBeVisible();
    expect(within(configuration).getByText("Target text")).toBeVisible();
    expect(within(configuration).getByText("Authorized reference speech")).toBeVisible();
    expect(within(configuration).getByText(/Live generation is unavailable/i)).toBeVisible();
    expect(within(configuration).getByText("Emotion category")).toBeVisible();
    expect(within(configuration).getByText("Emotion intensity")).toBeVisible();
  });

  it("requires a complete-method choice before dialogue preparation", () => {
    render(
      <MemoryRouter>
        <StudioShell onBack={vi.fn()} onRefresh={vi.fn()} project={{ ...selectedProject, method_selection: null }} />
      </MemoryRouter>,
    );

    expect(screen.getByRole("link", { name: "Open Method Atlas" })).toHaveAttribute("href", "/methods");
  });

  it("exports a selected-method preparation record only from a prepared local project", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      project_id: preparedProject.id,
      project_revision: preparedProject.revision,
      manifest_url: `/api/v1/projects/${preparedProject.id}/preparation-exports/revision-5/preparation.json`,
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);

    render(
      <MemoryRouter>
        <StudioShell onBack={vi.fn()} onRefresh={vi.fn()} project={preparedProject} />
      </MemoryRouter>,
    );

    const authorizationStatus = screen.getByLabelText("Preparation authorization status");
    expect(within(authorizationStatus).getByText("Video authorized")).toBeVisible();
    expect(within(authorizationStatus).getByText("Target text authorized")).toBeVisible();
    expect(within(authorizationStatus).getByText("Reference speech authorized")).toBeVisible();
    expect(screen.getByRole("button", { name: "Export preparation record" })).toBeEnabled();

    await user.click(screen.getByRole("button", { name: "Export preparation record" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    expect(fetchMock).toHaveBeenCalledWith(
      `http://127.0.0.1:8000/api/v1/projects/${preparedProject.id}/preparation-export`,
      { method: "POST" },
    );
  });

  it("shows an evidence-aware preparation context without changing the selected method boundary", () => {
    render(
      <MemoryRouter>
        <StudioShell onBack={vi.fn()} onRefresh={vi.fn()} project={preparedProject} />
      </MemoryRouter>,
    );

    const context = screen.getByRole("region", { name: "Preparation context" });
    expect(within(context).getByText("PREPARATION CONTEXT")).toBeVisible();
    expect(within(context).getByText("Video")).toBeVisible();
    expect(within(context).getByText("Text")).toBeVisible();
    expect(within(context).getByText("Authorized reference")).toBeVisible();
    expect(within(context).getByText("EmoDubber")).toBeVisible();
    expect(within(context).getByText("EVIDENCE-AWARE PREPARATION RECORD")).toBeVisible();
    expect(screen.getByText(/Live generation is unavailable/i)).toBeVisible();
  });

  it("uses the empty candidate lane to show a factual preparation trace rather than a fabricated output", () => {
    render(
      <MemoryRouter>
        <StudioShell onBack={vi.fn()} onRefresh={vi.fn()} project={preparedProject} />
      </MemoryRouter>,
    );

    const trace = screen.getByLabelText("Preparation trace");
    expect(within(trace).getByText("PREPARATION PATH")).toBeVisible();
    expect(within(trace).getByText("AUTHORIZED VIDEO")).toBeVisible();
    expect(within(trace).getByText("DECLARED TEXT")).toBeVisible();
    expect(within(trace).getByText("AUTHORIZED REFERENCE")).toBeVisible();
    expect(within(trace).getByText("EmoDubber")).toBeVisible();
    expect(within(trace).getByText("VERIFIED ADAPTER REQUIRED")).toBeVisible();
  });
});
