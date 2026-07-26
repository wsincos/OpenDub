# OpenDub From-Zero Launch Playbook

This is the execution entry point when the instruction is **"start implementation"**. It converts the locked OpenDub direction into a sequence of small, verifiable changes. Do not skip ahead to model execution or video editing before the earlier gates are satisfied.

## 0. Read before touching code

Read these documents in this exact order:

1. [`../00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md`](../00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md)
2. [`../00_PRODUCT/TASK_DEFINITION.md`](../00_PRODUCT/TASK_DEFINITION.md)
3. [`../01_CAPABILITIES/METHOD_EXPERIENCE_SPEC.md`](../01_CAPABILITIES/METHOD_EXPERIENCE_SPEC.md)
4. [`../02_ARCHITECTURE/ATLAS_CONTRACTS.md`](../02_ARCHITECTURE/ATLAS_CONTRACTS.md)
5. [`STATUS.md`](STATUS.md)
6. [`QUALITY_PLAN.md`](QUALITY_PLAN.md)

Then inspect the working tree and run the existing checks. Preserve unrelated user changes. Do not commit private reference media, checkpoints, credentials or the `reference/` research-notes directory.

### Required initial commands

```bash
git status --short
python -m pytest -q
npm exec --yes pnpm@9.15.0 -- --filter @opendub/web test -- --run
npm exec --yes pnpm@9.15.0 -- --filter @opendub/web run check
npm exec --yes pnpm@9.15.0 -- --filter @opendub/web run build
```

If the environment already contains a project-specific command that supersedes one of these, document the replacement in `STATUS.md`. A command is not a pass merely because it starts; save its exit status and relevant output in the implementation record.

## 1. Execution rules

### Work in vertical slices

Each slice must contain:

1. an acceptance test that initially fails for the expected reason;
2. the smallest implementation needed for that behavior;
3. unit/component tests and a route-level browser check;
4. desktop and mobile visual review;
5. a status update and an intentional commit.

Do not make a single large UI rewrite with no checkpoints. Do not introduce an abstraction merely because it could be shared later; method-specific Concept Labs are intentionally different.

### Truthfulness rules enforced during every slice

- A `Concept` control changes an explanation only.
- A `Replay` control chooses an existing recorded result only.
- A `Live` control must point to a successfully recorded run manifest.
- No absent data may be represented by random numbers, looping waveforms or generic neural-network animation.
- No audio player becomes active until the asset's rights, source and hash records exist.

### Source-of-truth hierarchy

```text
primary paper / fixed upstream source
        -> checked Method Manifest
        -> validated public content record
        -> frontend route
        -> recording script and grant prose
```

Correct the manifest and its review record before correcting the UI when they disagree.

## 2. Milestone map

| Milestone | User-visible outcome | Hard gate | Suggested release name |
|---|---|---|---|
| M0 | audited, reproducible project baseline | all current checks have a recorded result | `baseline` |
| M1 | task is understandable in 15 seconds | Task Explorer works without GPU/API | `atlas-task` |
| M2 | each complete method is deeply inspectable | three reviewed Concept Canvases | `atlas-methods` |
| M3 | evidence can be inspected and pages are recording-ready | no placeholders or unlabelled claims in recording path | `atlas-recording` |
| M4 | same-input recorded result comparison | common-input and public-rights gate | `atlas-replay` |
| M5 | one real complete-method local run | Live admission gate | `atlas-live-<method>` |

M3 is sufficient to make a truthful, polished grant video. M4 and M5 enhance it only when their evidence gates pass.

## 3. M0: baseline, content registry and review ledger

### Deliverables

- Verify the repository, frontend and Python test baseline.
- Fix or document any pre-existing failure before adding new product behavior.
- Validate the three method manifests using the Atlas validator.
- Record one fixed upstream source revision, paper URL, code license, checkpoint status and reviewer for each method.
- Create/maintain an evidence ledger that does not publish local paths or unverified download URLs.

### Tests and checks

- Python manifest parser rejects a method with missing paper, source revision, status or node edge.
- Browser content registry renders exactly three `core` methods.
- Any legacy/supporting repository is absent from the selector.
- Link checker confirms public paper/source links are valid.

### Stop condition

Do not write visual claims for a component whose paper wording, relation or name has not been checked. Mark it `pending review` instead.

## 4. M1: Task Explorer, the task-first opening

### Build order

1. Add `/explore` as the default route and a stable app shell.
2. Implement the four input tiles: `Video`, `Text`, `Reference Voice`, `Optional Control`.
3. Implement two visibly separate output tabs: `Target Speech` and `Dubbed Video`.
4. Add the readable task equation, with a formal-view disclosure rather than a mathematical hero.
5. Add a shared timeline primitive using integer microseconds and a keyboard-accessible cursor.
6. Add a method handoff that preserves the chosen method and the current time.

### Acceptance behavior

- A visitor can name all three required inputs without visiting a method page.
- Selecting the output tab never claims that the research model directly generates a video.
- No GPU/API is needed to render the full task explanation.
- A reduced-motion user receives state changes rather than continual decorative animation.

### Required tests

- default route and deep links;
- selecting each input changes its accessible explanation;
- `Target Speech` and `Dubbed Video` are distinguishable accessible tabs;
- the timeline responds to keyboard left/right and exposes its current value;
- 1440x900 and 390x844 visual snapshots contain all key labels without overlap.

## 5. M2: semantic graph foundation and the three Concept Canvases

### Common foundation, built once

1. Build a manifest-driven method registry and semantic validator.
2. Render nodes as actual buttons with an accessible label such as `Inspect Face Affect`.
3. On selection, highlight only verified upstream/downstream edges and render a typed inspector.
4. Provide a `Pin signal` action and an honest unavailable-signal state.
5. Keep canvas node dimensions and edge paths deterministic across target viewport sizes.
6. Add paper/source/citation actions and a visible content-mode badge.

### HPMDubbing slice

Implement the `Hierarchy Lens` described in `METHOD_EXPERIENCE_SPEC.md`:

- Lip, Face and Scene are three distinct selectable visual roles.
- Selection updates a text explanation and the highlighted relation.
- The relationship between visual layers and duration, F0/energy and global emotion is exact to the approved manifest.
- Curves remain labelled illustrative until valid data exists.

### StyleDubber slice

Implement the `Multi-scale Alignment Lens`:

- Frame-scale and phoneme-scale are an accessible segmented control.
- The visible intervals change but remain on the same overall time extent.
- A selected phoneme highlights the corresponding group of frames.
- MPA, PLA and USL retain their exact names and distinct roles.

### EmoDubber slice

Implement the `Emotion Guidance Lens`:

- Emotion category is a segmented control and intensity is a labelled range input.
- The explanation changes without activating invented audio.
- Positive and negative guidance are clearly distinguished.
- The `No new audio generated in Concept mode` boundary is permanently visible.

### Required tests

- one test per canvas selects at least two nodes and asserts the inspector explanation changes;
- one test per Concept Lab operates its unique control using accessible names;
- tests assert no Concept page inserts an `audio` element merely from a conceptual control;
- a11y tests find unambiguous names for graph nodes and controls;
- visual tests cover all three canvases at 1440x900, 1920x1080 and 390x844.

## 6. M3: Evidence Room and recording-ready polish

### Evidence Room

Add `/evidence` and link to it from every method page. For every core method show:

```text
Paper -> source repository -> source revision -> code license
      -> checkpoint terms -> content mode -> runtime status -> verification date
```

The correct result for unavailable weights is a compact, explicit warning such as `Weight terms unavailable; Live disabled`, not a broken download button.

### Recording-path polish

- Ensure `/explore`, `/methods`, all three `/methods/:slug`, `/compare`, `/evidence` have no empty panels, debug labels or inaccessible controls.
- Ensure the status label remains visible during any screen recording.
- Use actual cropped imagery, diagrams or signal geometry rather than text-only explanation cards.
- Configure reduced motion and stable initial screen state so retakes reproduce the same framing.
- Capture screenshots from a production build, not only the development server.

### Required checks

- every visible claim on the recording path maps to a paper/source/evidence record;
- browser route crawl has no console error, blank graph or broken link;
- visual QA signoff captures desktop and mobile images;
- no `Live` string appears on a method whose runtime is unavailable.

## 7. M4: Replay and Comparison Lab, only after the gate opens

### Preflight gate

For two candidate outputs, prove identical values for:

```text
video file hash
video crop/time range
target text normalization hash
reference-speech hash and selected range
preprocessing version
```

Also record output hashes, method/source revision, generation parameters, rights and reviewer.

### Implementation

1. Build the public Replay Bundle validator before the player.
2. Keep video shared once; candidates are mutually exclusive audio tracks on the same time cursor.
3. Add a blind-listen mode that masks method names until an explicit reveal.
4. Render only metrics valid for the same input and unit/preprocessing definition.
5. Export a comparison report with all status and hash evidence.

### Gate failure behavior

The `/compare` route remains a professional evidence-gate explainer. It must not show fabricated A/B audio, fake score cards or a global model ranking.

## 8. M5: optional Live integration

### Checkpoint audit procedure

Before downloading or using any checkpoint:

1. use the upstream repository and primary documentation to locate the candidate;
2. record source revision, code license, explicit weight terms, URL, filename and expected hash;
3. confirm the checkpoint can legally be downloaded, used and demonstrated;
4. use an isolated method environment; do not mutate the platform environment;
5. run one authorized smoke input and store its complete run manifest;
6. hash generated media and any exported signal; retain log and environment version;
7. have a method owner review the generated artifact before public release.

If no candidate meets all seven points, skip Live without weakening M1-M3. The product and film remain valid as a Concept Atlas.

### Live first-method selection rule

Choose the first method by *admission evidence*, not by visual preference. EmoDubber may be evaluated first because its user-control interaction is valuable, but it gets no exception to licence, hash or smoke-test requirements.

## 9. M6: final video and application handoff

Use the production package under [`../04_OPEN_SOURCE/DEMO_FILM/`](../04_OPEN_SOURCE/DEMO_FILM/). Do not start editing before M3 is signed off.

The recording order is:

1. task explanation;
2. method selection;
3. HPM hierarchy interaction;
4. Style scale interaction;
5. Emo control interaction;
6. evidence/status proof;
7. optional Replay/Live branch only if its gate passed.

Record the route, selected method, content status, browser size, source commit and asset manifest for every shot. The final video must be reproducible from the committed release tag.

## 10. Completion record

Update [`STATUS.md`](STATUS.md) at the end of every milestone using this format:

```markdown
## M<N> <name> - <date>

- Commit: `<sha>`
- Routes/assets changed: ...
- Evidence: tests ..., visual QA ..., content validation ...
- Status truth: Concept / Replay / Live / Planned
- Known limitation: ...
- Next gate: ...
```

Only mark a milestone complete when its stated acceptance tests, evidence requirements and visual checks have actually passed. A UI that looks polished but lacks a paper/source/status trail is not complete.
