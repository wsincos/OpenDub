# OpenDub Implementation Status

**Last updated:** 2026-07-25  
**Repository state:** `v0.0.1-alpha.0` development baseline  
**Truth rule:** a research upstream remains unavailable until source, weight, license, input contract,
and real inference evidence are all recorded.

## Completed In This Alpha

| Area | Delivered evidence |
| --- | --- |
| Governance and provenance | Apache-2.0 project governance, fixed upstream commits, registry validation, enforceable research-backend admission gate, EmoDubber/HPM/StyleDubber/HDCode audits |
| Project core | UUIDv7 IDs, microsecond ranges, versioned `project.json`, optimistic concurrency, rebuildable index, content-addressed assets |
| Media foundation | Safe FFprobe/FFmpeg calls, audio normalization, SRT/VTT import, deterministic audio assembly, explicit mix policies, MP4 `AI-generated dubbing by OpenDub` metadata, and a matching traceable render manifest |
| Authorization | A voice reference requires an in-project audio asset, material-source declaration, purpose, and explicit opt-in before generated output may be shared; every render records the aggregate distribution decision |
| Runtime contracts | Capability contract, verified-weight manager, JSON Lines isolated runtime, persistent local job primitives, run manifests |
| Recoverable pipeline | Four explicit prepare/generate/postprocess/evaluate stages, chained provenance cache keys, retry-safe atomic cache results, and cooperative cancellation |
| Candidate quality reports | Deterministic duration, silence, and clipping checks plus local JSON/Markdown reports; unavailable neural metrics remain explicitly unavailable |
| Test-only generation | Deterministic sine-wave fixture validates candidate persistence and traceability; it is not a user model |
| API and CLI | Local project management, asset serving, authorization, segment creation, registry listing, candidate acceptance, accepted-candidate render/download API, candidate evaluation/report API, durable job list and SSE event replay, `init`, `create`, `list`, `doctor`, `evaluate`, `render`, `serve` |
| Web Studio | Real local project list, media import, authorization recording, segment setup, local video preview, data-driven timeline, candidate audio review/evaluation/accept controls, explicit original-audio export policy, render evidence links, and visual QA |
| Documentation and grant | Quick start, model-status guide, grant summary, evidence index, alpha demo script, validated separate DOCX draft |
| Examples and delivery | Two FFmpeg-generated redistributable example projects, container definitions, Compose syntax check, documentation-link validation, and a GitHub Actions quality workflow |

## Deliberately Not Claimed As Complete

| Capability | Why it is blocked | Required evidence |
| --- | --- | --- |
| Real EmoDubber generation or emotion strength | Upstream code/weights do not yet meet the admission gate | Authorized immutable weights, license terms, isolated inference, control-effect test |
| HPMDubbing raw-video inference | Published workflow depends on dataset-specific features and restricted material | Authorized preprocessing fixture, exact feature contract, real smoke |
| StyleDubber backend | Checkpoints and preprocessing are not reproducibly admissible yet | Hashed weights, terms, fixture, isolated adapter, real smoke |
| Stable vocoder | Weight terms and compatibility smoke are absent | Hashed weights, mel contract, output validation |
| Candidate A/B product review | Requires a verified user-facing backend | Real candidates, metrics, acceptance/revision UI QA |
| Full content/speaker/emotion evaluation | Metric models and reference fixtures are not yet pinned | Versioned model weights, language limits, direction tests |
| Formal demonstration WAV/MP4 and film | The export service exists, but the public film must use genuine accepted candidates and authorized media | M2 adapter/metrics/export evidence and film QA |
| `v0.1.0` release | Real model gate and release validation are incomplete | All M2/M3 requirements in `DEFINITION_OF_DONE.md` |

## Current Verification

- `make check`: 88 tests pass, including a real FFmpeg/FFprobe check of exported MP4 provenance metadata; it also runs Ruff, mypy, TypeScript, and local documentation-link validation. The test run has one upstream FastAPI/Starlette `TestClient` deprecation warning only.
- Browser QA: empty and configured project states were captured at 1440×900; the configured flow imported local synthetic audio, recorded authorization, imported/editable subtitle cues, retained a compact cue timeline at 375×812, and kept Export gated without accepted candidates. An isolated `opendub.test` QA fixture also verified candidate evaluation, acceptance persistence, audio-policy selection, WAV download, manifest link, and non-distributable export status; it is not a product model or demo asset.
- DOCX: `original/output/种子计划_OpenDub_申报表_草案.docx` is generated from the original template by `tools/grant-docx/`, OpenXML-validated, and visually checked as a two-page A4 PDF.
- Docker: `docker compose config --quiet` passes. Image build was not run in this environment because access to the Docker daemon is denied.

## Next Execution Gate

Do not advance to a “real generation” demo until the project owner supplies or identifies a
redistributable checkpoint with explicit terms and SHA-256. The next implementation action is then
to build a single isolated adapter around that exact artifact, smoke-test it on authorized media,
and update `model-registry/upstreams.yaml`, its model card, the evidence index, and the demo script
from `planned` to the verified state supported by the result.
