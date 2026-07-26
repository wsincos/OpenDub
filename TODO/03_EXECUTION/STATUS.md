# OpenDub Implementation Status

**Last updated:** 2026-07-26

**Current application positioning:** [OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台](../00_PRODUCT/PLATFORM_POSITIONING.md)

**Repository state:** `v0.0.1-alpha.0`; the three-method Concept Atlas, evidence-bound method selection, authorized local project preparation, and preparation export are implemented. Replay and Live remain evidence-gated.

## Verified Current Foundation

| Area | Verified state |
|---|---|
| platform governance | Apache-2.0 code, source/weight audit records, responsible-use documentation |
| local project foundation | versioned project state, content-addressed assets, authorization records, microsecond timeline, FFprobe/FFmpeg utilities |
| platform runtime | local API, CLI, Studio, model registry, isolated-adapter contract, job/run records |
| Atlas front end | Task Explorer, Method Atlas, three complete method canvases, method-specific Concept interactions, Evidence Room, evidence-gated comparison route |
| content integrity | three validated Method Manifests, fixed source commits, public source-license records, current checkpoint audit |
| quality | `108` Python tests, `21` web tests, manifest validation, Registry validation, documentation links, production build, Word/OpenXML validation, and desktop/mobile visual QA passed on 2026-07-26 |

## Current Public Truth

| Capability | State | Permitted claim |
|---|---|---|
| task explanation and method interaction | Concept | users can understand and inspect the three methods interactively |
| method selection | Concept | users can make an evidence-aware selection and prepare a project; the record is validated against the fixed method manifest |
| local project/media/authorization workflow | implemented | users can retain a selected complete method, record current video/text/reference-speech authorization, and export a preparation manifest |
| public same-input comparison | evidence-gated | interface and fairness rules exist; no qualified multi-method result is published |
| genuine model generation | unavailable | no listed research method is currently advertised as Live in OpenDub |

## Next Work: Application-First Order

1. **P3 recording action:** use the prepared script and authorized demo material to record the human-submitted application video; all code, document, and QA prerequisites are complete.
2. **P4:** only after qualifying authorized Replay bundles exist, unlock genuine cross-method comparison.
3. **P5:** only after a complete method passes the admission gate, expose one local Live run.

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
