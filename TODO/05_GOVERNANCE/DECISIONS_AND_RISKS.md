# Decisions, Gates, and Risks

## Accepted Decisions

| ID | Decision | Reason |
|---|---|---|
| D1 | OpenDub is an AIGC video-dubbing platform, not a new hybrid model. | gives the grant one coherent open-source project with a credible engineering boundary |
| D2 | Interactive visualization and Method Atlas are the primary product entry and method-selection workspace. | this is the distinctive contribution and remains useful without a checkpoint |
| D3 | HPMDubbing, StyleDubber, and EmoDubber remain the only first-class complete methods. | preserves research validity and makes the first release understandable |
| D4 | Studio retains a selected complete method and authorized project inputs. | connects the Atlas to practical AIGC use without falsely claiming runtime availability |
| D5 | P0-P3 are the application release; Replay and Live are conditional P4/P5 upgrades. | simplest credible scope under current evidence |
| D6 | LLM orchestration, multilingual, multi-character, and hardware expansion are roadmap items. | avoids inflating the seed-grant deliverable |

## Evidence Gates

### Gate A: Method accuracy

A method card or Canvas claim needs primary-paper/fixed-source evidence and reviewer approval. Without it, the claim is removed or labelled planned.

### Gate B: Public Replay

Replay needs authorized media, input/output hashes, source revision, rights record, and reviewer approval. Without it, Compare remains an evidence explainer.

### Gate C: Fair Comparison

Two results must share video, crop/time window, normalized text, reference-speech range, preprocessing version, and listening policy. Without it, they are not displayed as a comparison set.

### Gate D: Live Admission

Live needs code license, weight terms, expected hash, authorized smoke input, isolated environment, successful real run, output hash, and a retained run manifest. A download link or paper demo is insufficient.

### Gate E: Application Freeze

Form, repository, release commit, documentation, screen recording, and film script must agree on the same capability state and official project identity.

## Risk Register

| Risk | Effect | Mitigation |
|---|---|---|
| unavailable or unclear checkpoint | blocks Live | keep P0-P3 independent; audit before any integration |
| no shared-input public outputs | blocks fair comparison | keep evidence-gated Compare; seek rights-cleared Replay later |
| platform appears to be only a paper gallery | weakens application value | demonstrate selection handoff and authorized local project preparation |
| platform appears to promise one unified model | scientific and credibility risk | retain complete-method language and visible method boundaries |
| unauthorized sample media or voice | legal and ethical risk | rights register, local-first flow, and pre-publication review |
| too many future features | delivery risk | P0-P3 scope lock; roadmap items do not enter acceptance criteria |

## Change Rule

Any proposal to add a core method, declare a new status, change the platform name, or make P4/P5 mandatory must update this document, `PLATFORM_POSITIONING.md`, `SCOPE_LOCK_AND_PRODUCT_DECISION.md`, grant prose, and the film script before implementation begins.
