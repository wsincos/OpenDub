# OpenDub Implementation Status

**Last updated:** 2026-07-27

**Current application positioning:** [OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台](../00_PRODUCT/PLATFORM_POSITIONING.md)

**Repository state:** `v0.0.1-alpha.0` is the released V1 baseline. The separately scoped [V2 cinematic VTTS showcase redesign](../07_V2_SHOWCASE/README.md) is implemented in the current working tree and is undergoing release QA and independent review. Replay and Live remain evidence-gated.

## Verified Current Foundation

| Area | Verified state |
|---|---|
| platform governance | Apache-2.0 code, source/weight audit records, responsible-use documentation |
| local project foundation | versioned project state, content-addressed assets, authorization records, microsecond timeline, FFprobe/FFmpeg utilities |
| platform runtime | local API, CLI, Studio, model registry, isolated-adapter contract, job/run records |
| Atlas front end | Task Explorer, Method Atlas, three complete method canvases, method-specific Concept interactions, Evidence Room, evidence-gated comparison route |
| content integrity | three validated Method Manifests, fixed source commits, public source-license records, current checkpoint audit |
| quality | `108` Python tests, `22` web tests, manifest validation, Registry validation, documentation links, production build, Word/OpenXML validation, and desktop/mobile visual QA passed for the V1 release |

## Current Public Truth

| Capability | State | Permitted claim |
|---|---|---|
| task explanation and method interaction | Concept | users can understand and inspect the three methods interactively |
| method selection | Concept | users can make an evidence-aware selection and prepare a project; the record is validated against the fixed method manifest |
| local project/media/authorization workflow | implemented | users can retain a selected complete method, record current video/text/reference-speech authorization, and export a preparation manifest |
| public same-input comparison | evidence-gated | interface and fairness rules exist; no qualified multi-method result is published |
| genuine model generation | unavailable | no listed research method is currently advertised as Live in OpenDub |

## V2 Release Gate

1. **V2 release QA:** validate two manifest-approved historical cases, feature derivation, `/vtts`, Example Gallery, V2 film and five viewport captures.
2. **V2 audit:** receive an independent strict review of application eligibility, factual boundaries, visual hierarchy and film effectiveness; resolve any score below `9/10`.
3. **V2 publication:** make a scoped V2 commit, tag only after clean-clone verification, and preserve the V1 tag untouched.
4. **P4:** only after qualifying authorized Replay bundles exist, unlock genuine cross-method comparison.
5. **P5:** only after a complete method passes the admission gate, expose one local Live run.

## Evidence Boundary

Candidate checkpoint files, public paper demos, or source repositories are not enough to change a method to Live. The upgrade requires explicit weight terms, expected hash, authorized input, isolated environment, successful smoke run, output hash, and a retained run manifest. Details are in `docs/atlas/checkpoint-audit-2026-07-26.md`.

## Update Format

Append a short record after each completed phase:

```markdown
## P<N> <outcome> - YYYY-MM-DD

- Commit: `<sha>`
- User-visible change: ...
- Evidence: tests / visual QA / source review ...
- Public state: Concept / Replay / Live / Planned
- Known limitation: ...
- Next phase or gate: ...
```

## P1 Method Selection - 2026-07-26

- User-visible change: Atlas and Method Canvas pages pass a chosen complete method into Studio; Studio preserves an evidence-bound selection record.
- Evidence: method-selection unit/integration tests, all-three-method validation, and web route tests.
- Public state: `Concept`; selecting a method never claims that it can generate now.
- Known limitation: no complete method is currently admitted for Live execution.
- Next phase: P3 application-material freeze and the prepared human recording action.

## P2 Authorized Preparation Export - 2026-07-26

- User-visible change: Studio shows the selected method and declared requirements, records input confirmations, and exports `opendub.project-preparation/v1`.
- Evidence: preparation-service/API tests and Studio component tests; export validates current video hash, target-text fingerprint, reference-speech consent, and method consistency.
- Public state: `Concept`; exported data is a handoff record, not an inference job.
- Known limitation: Replay and Live remain blocked by their independent evidence gates.
- Next phase: P3 application-material freeze and the prepared human recording action.

## P3 Application Materials and QA - 2026-07-26

- User-visible change: project identity, README, quick start, grant summary, evidence index, recording script, platform architecture asset, and a new filled Word-form copy all use the application positioning.
- Evidence: `make check` (`108 passed`), web tests (`21 passed`), production build, three-manifest validation, Registry validation, link check, OpenXML validation, and desktop/mobile browser screenshots.
- Public state: the release remains `v0.0.1-alpha.0`; the material does not claim Replay or Live availability.
- Known limitation: final application video capture requires an authorized recording session; its complete script and fact boundary are ready in `docs/grant/demo-script.md`.
- Next phase: P4 or P5 only after their evidence gates; recording can proceed immediately without a checkpoint.

## P6 V2 Task-First Showcase - 2026-07-27 (release QA in progress)

- User-visible change: the default route is now `/vtts`, a dynamic explanation of `Video + Target Text + Authorized Reference Speech -> Complete Method -> Target Speech + Dubbed Video`. It includes Face/Lip/Environment inspection, a GT-derived feature display, a two-case four-panel historical example gallery, and direct links into the independent complete methods.
- Evidence: two versioned case manifests, SHA-256 verified source media copies, deterministic feature generation, Python manifest/feature tests, React behavior tests, V2 caption-led film and delivery metadata.
- Public state: the cases are `Archived research example`; the stage itself is `Task illustration`. Neither is a fresh OpenDub run, a Replay bundle, or a fair same-input benchmark.
- Known limitation: the supplied cases lack canonical transcript / IPA contracts, so their IPA is deliberately unavailable. The visible IPA on `/vtts` is labeled task notation and does not claim to describe the case media. The V2 film is ready for an optional human narration recording pass and is already usable as a caption-led delivery.
- Next gate: rebuild final captures after visual QA, run the complete verification suite, and obtain the V2 strict audit before creating a V2 release commit/tag.
