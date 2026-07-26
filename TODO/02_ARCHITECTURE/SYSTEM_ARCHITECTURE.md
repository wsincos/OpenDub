# OpenDub Platform Architecture

## Architecture Objective

OpenDub is an open-source AIGC video-dubbing platform whose interactive Atlas is the primary user interface. The architecture must support two related but independently useful loops:

```text
Interactive selection loop
  task explanation -> method catalog -> component inspection -> evidence-aware choice

Project and use loop
  local project -> authorized inputs -> selected complete method
                -> Concept / Replay / verified Live -> record / compare / export
```

The loops meet at a **selected complete method**. They must never meet by merging internal neural modules from different research methods.

## Four Planes

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ Interaction and Selection Plane                                          │
│ Task Explorer | Method Atlas | Method Canvas | Evidence | Compare | UI  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ selected method + typed content
┌────────────────────────────▼────────────────────────────────────────────┐
│ Method and Content Plane                                                 │
│ Method Manifest | capability catalog | Concept assets | Replay bundles   │
│ graph validation | citations | status | selection requirement contract   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ project preparation / optional execution
┌────────────────────────────▼────────────────────────────────────────────┐
│ Local Project and Runtime Plane                                          │
│ project.json | media | authorization | timeline | adapters | jobs        │
│ runs | output rendering | CLI | FastAPI | Web Studio                     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ proof for every public claim
┌────────────────────────────▼────────────────────────────────────────────┐
│ Evidence and Governance Plane                                            │
│ papers | fixed source commits | licenses | weight status | rights | QA   │
│ hashes | reviewer record | release / film claim index                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Interaction and Selection Plane

### Required routes

| Route | User outcome |
|---|---|
| `/explore` | understand the multimodal task and move into the catalog |
| `/methods` | compare the declared focus, controls, constraints, and status of complete methods |
| `/methods/:methodId` | inspect one complete method and select it for a project |
| `/evidence` | inspect paper, source, license, weight, rights, and runtime evidence |
| `/studio` | prepare a local authorized project and retain the selected method |
| `/compare` | inspect qualified same-input results; otherwise explain the gate |

The Atlas uses real semantic controls, stable graph layout, a shared time reference, and mode labels. Its output is a **MethodSelectionRecord**, not a model invocation.

### MethodSelectionRecord

```ts
type ContentMode = "concept" | "replay" | "live" | "planned";

interface MethodSelectionRecord {
  methodId: "galaxycong/hpmdubbing" | "galaxycong/styledubber" | "galaxycong/emodubber";
  methodManifestVersion: string;
  selectedAt: string;
  declaredNeed: string;
  requiredInputs: string[];
  optionalControls: string[];
  runtimeStatus: "unavailable" | "experimental" | "stable";
  contentModes: ContentMode[];
  evidenceRevision: string;
}
```

Studio stores this record with the project revision. A Project may prepare an input for a method that is currently unavailable; it cannot start a job until a verified adapter is admitted.

## Method and Content Plane

The structured Method Manifest is the source for method cards, graphs, Evidence Room, selection requirements, and developer documentation. It contains:

- complete input/output contract;
- capability declarations and selection wording;
- graph nodes, true data-dependency edges, and explainable signal slots;
- paper, fixed upstream source, license, checkpoint, and reviewer evidence;
- `Concept` / `Replay` / `Live` / `Planned` status;
- required and optional project-preparation fields.

`CaseManifest` and `ReplayBundle` are optional content types. They are not needed to render Concept, but a public comparison cannot render without qualifying cases and result bundles.

## Local Project and Runtime Plane

The existing local-first platform foundation remains the execution base:

- `project.json` and revision control are the project truth source;
- media is content-addressed and processed through parameterized FFprobe/FFmpeg calls;
- video, script, reference speech, time window, rights, and selected-method record form a prepared project;
- FastAPI, CLI, and Studio expose the local project workflow;
- each admitted complete method runs in its own isolated Adapter environment;
- a run records inputs, source revision, environment, parameters, output hashes, and genuine registered intermediate artifacts.

An adapter may use its own upstream preprocessing and vocoder dependencies. It may not pull internals from another core method to satisfy its contract.

## Evidence and Governance Plane

Every public status must be derived from versioned facts, not hand-authored marketing copy:

```text
paper + fixed source + code license
    + weight terms/hash (when applicable)
    + input/output rights
    + smoke or replay evidence
    -> public content and runtime status
```

Evidence Room, grant prose, recording captions, model-status documents, and release notes consume this same record. Any disagreement is corrected in the manifest/evidence record first.

## Deployment Modes

| Mode | Includes | Does not claim |
|---|---|---|
| static Atlas | Task Explorer, catalog, Concept Canvases, Evidence, documented project handoff | that users can locally run an unavailable method |
| local platform | static Atlas plus FastAPI, Studio, local project/media workflow | that a checkpoint is admitted by default |
| verified method extension | local platform plus one isolated complete-method adapter and run record | that other methods have become Live |

The application release uses the static Atlas and local platform modes. The verified extension mode is a gated future release.

## Failure Rules

- Missing checkpoint or runtime: preserve method selection and show the evidence reason; never replace it with simulated output.
- Missing public Replay: Comparison displays the admission requirements and remains non-ranking.
- Missing visual signal: show the component explanation and an explicit absence reason.
- Unauthorized reference speech: block run/export eligibility and retain a clear remediation action.
- API unavailable: Concept remains usable; Studio shows a local-service state rather than an empty interface.

## Extension Boundary

New complete methods enter through a Method Manifest, evidence review, project-preparation contract, and optional Replay/Adapter integration. This creates an open ecosystem without requiring a new platform release for every paper-specific implementation.
