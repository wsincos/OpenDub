# OpenDub Application-First Implementation Plan

> This master plan is intentionally small. It is the implementation order for the seed-grant platform, not a promise to build every future AIGC workflow at once.

**Goal:** deliver a truthful, usable open-source platform in which the interactive Atlas is the method-selection front door and Studio is the local project-preparation workbench.

## Operating Rules

- Preserve HPMDubbing, StyleDubber, and EmoDubber as separate complete methods.
- Build the user path before optional model integrations: understand -> select -> prepare -> inspect -> run only when admitted.
- Treat all Concept media as explanation, not output.
- Keep Replay and Live behind their evidence gates.
- Make one focused vertical slice at a time, with tests, visual review, documentation update, and an intentional commit.

## P0: Baseline Already Implemented

**Status:** verified foundation exists; do not rebuild it.

- local project/media/authorization and timeline primitives;
- API, CLI, Studio, model registry, adapter contract, rendering/run records;
- Task Explorer, three Method Canvases, Evidence Room, and evidence-gated Compare route;
- manifests, tests, CI, and a current checkpoint audit.

Before any new work, run the project checks and read [STATUS.md](STATUS.md). Fix an existing regression before starting a new phase.

## P1: Make Atlas the Method-Selection Front Door

**Status:** completed in the application-release working tree on 2026-07-26.

**Outcome:** an AIGC creator or reviewer can go from a declared goal to one informed complete-method selection.

1. Freeze the application name, one-sentence statement, input/output terminology, and status vocabulary across README, Atlas, docs, and grant copy.
2. Add or verify a catalog view that expresses each method's focus, declared user control, current content/runtime state, source, and limitations.
3. Add a `Prepare project` handoff from each method card and method page.
4. Persist a validated `MethodSelectionRecord` containing method ID, manifest revision, declared need, required inputs, optional controls, and evidence revision.
5. Ensure every selection recommendation says “inspect/select first” rather than “best” or “generates now.”

**Delivered:** every core Atlas card and Canvas has a `Prepare project` route. The local project stores a validated selection with method ID, fixed manifest/evidence revision, declared need, required inputs, optional controls, runtime status, and content mode. The API refuses stale or mismatched manifest evidence.

**Acceptance:** a route-level test confirms that choosing each of the three methods creates the correct selection record, and desktop/mobile visual review shows the handoff without hiding the content-status label.

## P2: Connect Selection to a Useful Local Project

**Status:** completed in the application-release working tree on 2026-07-26.

**Outcome:** the platform becomes usable before a checkpoint is admitted.

1. Extend the Studio project flow to accept a MethodSelectionRecord.
2. Display the selected method, required inputs, optional controls, and runtime/evidence status on the project screen.
3. Validate that the project has video, target text, authorized reference speech, time window, rights record, and selected method before it is considered prepared.
4. Export a project-preparation manifest that can be sent to a method owner or later passed to an admitted Adapter.
5. Make unavailable runtime a clear, non-destructive state: the project remains editable and exportable, but Run is disabled with the evidence reason.

**Delivered:** Studio displays the selected method, its declared requirements, and `Concept` status; it records a video authorization and target-text fingerprint, requires a consented reference speech for each segment, and exports an atomic `opendub.project-preparation/v1` manifest. The server recomputes hashes and rejects stale authorizations, missing consent, method mismatch, or ambiguous video input.

**Acceptance:** a user can choose each core method, create a local project with authorized inputs, save/reopen it, and export the selected-method preparation record without any model weight.

## P3: Freeze the Application Release

**Outcome:** the repository is immediately understandable and recordable as an AIGC platform.

1. Publish a project-level architecture diagram showing the Atlas/Studio/evidence relationship, not a fictional unified neural network.
2. Align README, quick start, model status, grant summary, application form, and evidence index with the application name and P0-P3 scope.
3. Record the required walkthrough: task -> method selection -> one Method Canvas interaction -> Evidence Room -> project preparation handoff.
4. Run automated checks, content validation, route crawl, desktop/mobile screenshot review, link check, and claim-to-evidence review.
5. Create a release candidate that names the commit, known limits, and verified state.

**Acceptance:** every screen and narration line in the application film maps to a source, test, or evidence record. No viewer can reasonably mistake Concept for a fresh generated result.

## P4: Replay and Fair Comparison (Conditional)

Start only after two authorized outputs satisfy the same-input gate: matching video hash and time range, normalized text hash, reference-speech hash/range, preprocessing version, rights record, source revision, and output hash.

**Outcome:** a user can inspect or blind-listen to qualified result bundles without an invalid global ranking.

## P5: First Verified Live Method (Conditional)

Start only after one complete method has a source revision, code license, usable weight terms, expected hash, authorized smoke input, isolated environment, successful real run, and run manifest.

**Outcome:** a user can initiate one new local run and inspect genuine registered artifacts. The other two methods keep their own existing status.

## Appendix Plans

The following detailed plans remain implementation references, but they must follow the P0-P5 sequence above:

- [Task Explorer plan](01_TASK_EXPLORER_PLAN.md): P1 interaction work.
- [Method Atlas plan](02_METHOD_ATLAS_PLAN.md): P1 catalog and Canvas work.
- [Comparison Lab plan](03_COMPARISON_LAB_PLAN.md): P4 only.
- [Live and content plan](04_LIVE_AND_CONTENT_PLAN.md): P5 only.
- [Quality plan](QUALITY_PLAN.md): applies to all phases.
