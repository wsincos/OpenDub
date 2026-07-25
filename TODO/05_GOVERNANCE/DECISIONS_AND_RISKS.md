# Decisions, Gates and Risks

## Accepted Decisions

| ID | Decision | Reason |
|---|---|---|
| ADR-001 | The unified project is named OpenDub | One project, one main repository and a clear grant boundary |
| ADR-002 | New platform code uses Apache-2.0 | OSI-recognized license with patent grant; upstream licenses remain separate |
| ADR-003 | Original method repositories remain independent | Preserve research history, licenses and authorship |
| ADR-004 | The product is Method Atlas, not a hybrid model | Combining internal modules would create an unvalidated system |
| ADR-005 | HPMDubbing, StyleDubber and EmoDubber are the only core methods | Strong technical continuity and manageable first release scope |
| ADR-006 | Task Explorer is the public default route | The task must be understood before a reviewer sees model names |
| ADR-007 | Concept, Replay, Live and Planned are separate content states | Avoid conflating paper explanation, history and running code |
| ADR-008 | Atlas works without API/GPU/checkpoint | The grant demo must remain accessible and resilient |
| ADR-009 | Replay is exportable only with media/voice rights evidence | Public demos must be legally sustainable |
| ADR-010 | Same-input hashes gate Comparison Lab | Different upstream demos cannot justify model ranking |
| ADR-011 | Live uses the existing isolated Adapter Runtime | Legacy Python/CUDA dependencies cannot contaminate the core app |
| ADR-012 | Visualization signals are declared and evidence-bound | No invented tensor animations or random values |
| ADR-013 | HPMDubbing_Vocoder is supporting infrastructure | It is not a fourth full video dubbing method |
| ADR-014 | Static Atlas and local Studio are separate experiences | Education/review should not depend on a GPU workflow |
| ADR-015 | The official film is task-first and status-labeled | A professional film must be impressive without overstating Live capability |
| ADR-016 | Main repository is `wsincos/OpenDub` | This is the owner-provided grant repository |

## Execution Gates

### Gate A: Core Method Accuracy

Before public Method Canvas release, a method reviewer approves every core node, edge, input/output description and citation for HPMDubbing, StyleDubber and EmoDubber.

Failing result: retain internal drafts; do not publish the affected Method Canvas as factual content.

### Gate B: Public Replay Rights

Every public bundle must pass asset-source, public-display, redistribution, hash and reviewer checks.

Failing result: display a Concept-only method page or keep Replay local; do not use it in film or downloadable release.

### Gate C: Same-Input Comparison

At least two result bundles must reference identical video, text, reference speech, crop and time-range hashes.

Failing result: Comparison Lab code remains available for fixtures, but public navigation shows the gate explanation rather than candidates.

### Gate D: Live Admission

One candidate method must provide a fixed source commit, explicit weight terms, SHA-256, authorized input fixture, isolated environment and real smoke evidence.

Failing result: runtime stays unavailable; Concept/Replay film path remains the release path.

### Gate E: Film Freeze

All recorded routes, asset rights, state labels, commit and content-lock are logged before editing.

Failing result: do not submit the film.

## Risk Register

| ID | Risk | Trigger | Response |
|---|---|---|---|
| R-001 | Paper-to-UI wording drift | reviewer corrects a node/edge | make manifests the source of truth and require author review |
| R-002 | Visual effects imply unavailable model data | Concept signal has no label | enforce `illustrative=true` and render mode badge |
| R-003 | Historical Demo lacks public rights | audit status unknown | exclude it; use self-created Concept assets |
| R-004 | No shared input outputs exist | comparison gate fails | do not rank methods; use branch B in film |
| R-005 | Checkpoint license is unclear | no explicit weight terms/hash | do not add Live and do not mirror weights |
| R-006 | Three methods become a superficial gallery | no deep node/signal interaction | require minimum nodes, signals, paper anchors and reviewer approval |
| R-007 | Graph is visually impressive but unreadable | overflow or overlap in visual QA | deterministic layout, stable node sizes and target viewports |
| R-008 | Media synchronization drifts | seek/switch exceeds 50ms | single TimelineController and browser E2E assertions |
| R-009 | Large signals freeze browser | low FPS or blank Canvas | lazy route loading, Canvas/WebGL and binary/on-demand arrays |
| R-010 | Scope expands to a production dubbing SaaS | account/cloud/realtime features appear | keep Atlas and local Studio scope, reject unrelated features |
| R-011 | Film overclaims current status | narration lacks evidence row | fact-check every sentence and retain badges |
| R-012 | Grant form claims planned UI as completed | application wording diverges from STATUS | use APPLICATION_FAST_TRACK wording table |

## Change Rules

Create a new ADR and update product, contracts, tests and grant material when changing:

- core method set;
- task input/output definition;
- content state semantics;
- replay rights policy;
- comparison gate;
- Adapter/VisualizationProvider protocol;
- public repository, license or release promise;
- grant-film claims.

Small internal visual changes may use a normal PR description only if they do not change meaning or status.
