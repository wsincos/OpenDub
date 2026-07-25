# Traceability Matrix

## Product Requirement to Evidence

| Requirement | Primary spec | Implementation plan | Proof |
|---|---|---|---|
| Accurate video dubbing task | TASK_DEFINITION | M1 Task 6 | component tests, equation inspection, user test |
| Three complete original methods | CORE_METHODS | M2 Task 1 | manifests, author review, Canvas E2E |
| Clickable components | METHOD_ATLAS_SPEC | M2 Tasks 3-4 | graph/inspector tests, Playwright |
| Time-aligned signals | VISUALIZATION_SIGNAL_MAP | M1 Task 5, M2 Task 5 | TimelineController and renderer tests |
| Honest Concept/Replay/Live | METHOD_ATLAS_SPEC | M1 Task 1, M4 Tasks 3/5/7 | validator, status tests, film QA |
| Same-input comparison | METHOD_ATLAS_SPEC | M3, M4 Task 4 | comparison gate, browser media tests |
| Evidence Room | SYSTEM_ARCHITECTURE | M2 Task 7 | status tests and content audit |
| Optional Live integration | SYSTEM_ARCHITECTURE | M4 Tasks 5-8 | real smoke and run manifest |
| Professional grant film | DEMO_FILM | M4 Task 10 | shot log, fact-check, delivery hashes |

## Complete Method Mapping

| Method | Full method contribution | Required Canvas nodes | Required signals | Evidence source |
|---|---|---|---|---|
| HPMDubbing | hierarchical Lip/Face/Scene prosody | lip_duration, face_affect, scene_emotion, hierarchical_prosody, mel_decoder, vocoder | Lip ROI, Face ROI, phonemes, duration, F0, energy, mel, waveform | CVPR 2023 + fixed code commit |
| StyleDubber | phoneme-level and utterance-level style | phoneme_view, mpa, pla, usl, mel_decoder, refinement | video, Lip ROI, phonemes, reference wave, alignment, mel, waveform | ACL 2024 + fixed code commit |
| EmoDubber | synchronization, pronunciation and user emotion control | lpa, pe, speaker_identity, emotion_control, fuec, pngm | Lip ROI, phonemes, reference wave, emotion control, waveform | CVPR 2025 + fixed code commit |

## State Rules

| UI status | Required evidence | Allowed film use |
|---|---|---|
| Concept | approved manifest and paper anchor | yes, with label |
| Replay | approved bundle, hash and rights | yes, with label |
| Live | ready runtime, fixed commit/weight hash and real smoke | yes, with label |
| Planned | route-map entry only | roadmap only |

## Current Alpha to Atlas Transition

| Existing asset | New use | First implementation task |
|---|---|---|
| Media/FFmpeg | case proxy, pack and output validation | M3 Task 1 |
| Model Registry | Evidence Room and Live admission | M2 Task 7, M4 Task 5 |
| Isolated runtime | complete Live Adapter | M4 Task 5 |
| Project/run manifests | Live-to-Replay traceability | M4 Task 8 |
| Web Studio | `/studio` route after Atlas shell | M1 Task 3 |
| Existing tests | regression baseline | M1 Task 1 onward |

## Grant Field Mapping

| Grant field | Source of truth | Current truthful status |
|---|---|---|
| Project title | GRANT_AND_DEMO | fixed |
| Technical foundation | CORE_METHODS + UPSTREAM_BASELINE | existing research/code |
| Current software base | STATUS | alpha implemented |
| Funded innovation | PROJECT_CHARTER | planned Atlas platform |
| Milestones | IMPLEMENTATION_PLAN | planned |
| Public evidence | Evidence Room + film | release-gated |
| Risks | DECISIONS_AND_RISKS | explicit |
