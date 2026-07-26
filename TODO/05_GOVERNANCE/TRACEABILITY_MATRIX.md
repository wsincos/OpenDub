# Traceability Matrix

## Application Requirement to Evidence

| Requirement | Product source | Delivery phase | Evidence |
|---|---|---|---|
| AIGC video-dubbing task is understandable | `TASK_DEFINITION.md` | P1 | route tests, accessible labels, visual QA |
| Atlas is a usable method-selection front door | `PLATFORM_POSITIONING.md` | P1 | selection tests, MethodSelectionRecord, recording route |
| three complete methods retain their own boundaries | `CAPABILITY_AND_MODEL_MAP.md` | P1 | manifests, graph validation, source review |
| selection carries into an authorized local project | `SYSTEM_ARCHITECTURE.md` | P2 | project save/reopen/export tests |
| evidence and status are truthful | `DECISIONS_AND_RISKS.md` | P1-P3 | manifest/status validation, Evidence Room review |
| documentation and application package are coherent | `GRANT_AND_DEMO.md` | P3 | link check, claim index, final review |
| same-input comparison is fair | `ATLAS_CONTRACTS.md` | P4 | case/replay validator and browser playback tests |
| one new local model output is real | `DOMAIN_CONTRACTS.md` | P5 | isolated smoke run and run manifest |

## Method Mapping

| Method | Role in OpenDub | Required public mode for P0-P3 | Conditional extension |
|---|---|---|---|
| HPMDubbing | visual-prosody selection and explanation | Concept | Replay or Live after its own gate |
| StyleDubber | multi-scale style selection and explanation | Concept | Replay or Live after its own gate |
| EmoDubber | emotion-guided selection and explanation | Concept | Replay or Live after its own gate |
| HPMDubbing_Vocoder | supporting infrastructure | documented support only | admitted only in its native complete-method context |
| LLM-Flow-Dubber | future orchestration route | Planned | separate tested roadmap |

## State Rules

| State | Required evidence | Permitted public statement |
|---|---|---|
| Concept | primary paper + fixed source | “interactive explanation of the method” |
| Replay | authorized result bundle + provenance | “recorded authorized result” |
| Live | full live admission gate + run manifest | “verified local generation” |
| Planned | roadmap entry | “planned future capability” |
