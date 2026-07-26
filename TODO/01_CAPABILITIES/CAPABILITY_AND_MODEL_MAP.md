# Complete-Method Catalog and Selection Map

## Purpose

This catalog powers the platform's method-selection experience. It helps a user choose and prepare **one complete method**. It is not a menu of interchangeable neural modules.

```text
declared user need -> inspect complete methods -> select one method -> prepare project
                                                   -> Replay / verified Live when admitted
```

## Catalog Entries

### First-class complete methods

| Method | Primary selection reason | User-visible interactive signature | Current status |
|---|---|---|---|
| HPMDubbing | understand visual cues for prosody | Lip / Face / Scene hierarchy lens | Concept |
| StyleDubber | inspect speaking style at multiple temporal scales | frame-to-phoneme and utterance-scale lens | Concept |
| EmoDubber | inspect explicit emotion category and intensity control | positive/negative emotion-guidance lens | Concept |

### Supporting infrastructure

| Asset class | Role | Public selector rule |
|---|---|---|
| HPMDubbing_Vocoder | acoustic support in its upstream context | never a peer method |
| face/lip preprocessing | input preparation or evidence | describe only when the selected complete method uses it |
| media, rendering, evaluation tools | platform infrastructure | do not present as a dubbing method |

### Planned routes

| Route | Intended role | First-release rule |
|---|---|---|
| LLM-Flow-Dubber | future script/role/emotion orchestration | roadmap only; no automation claim |
| multilingual and multi-character work | future content-production workflows | roadmap only |
| third-party method registry | external ecosystem extension | publish contract first, admit methods individually |

## Evidence-Bound Selection Questions

| User question | Method to inspect first | Required wording boundary |
|---|---|---|
| How do lip motion, facial affect, and scene context influence prosody? | HPMDubbing | “explains this hierarchical visual-prosody approach” |
| How are local pronunciation and global speaking style related? | StyleDubber | “explains this multi-scale style approach” |
| How is an explicit emotion category and intensity represented? | EmoDubber | “explains this controllable-emotion approach” |
| Which method is best? | all qualifying methods | no answer without a shared-input, qualifying comparison case |
| Can this method generate my new project now? | selected method | only say yes when that method has an admitted Live adapter |

## Capability Dimensions

The following dimensions may filter the catalog. They do not license component mixing:

- video-aware conditioning;
- lip and duration relationship;
- face or scene contribution;
- reference-speech identity condition;
- phoneme-scale or utterance-scale style representation;
- explicit user emotion category or intensity;
- current input constraints, runtime state, and evidence state.

Each capability declaration must cite a paper or fixed upstream source. A `Concept` card may explain a capability even when its runtime is unavailable.

## Method Admission Contract

A method enters the catalog only when it has all of the following:

1. a stable ID, a primary paper or technical report, and a fixed upstream source revision;
2. a complete input-to-output definition that does not depend on another core method;
3. a component graph with source-backed explanations;
4. code, weight, asset, and output-rights status records;
5. an explicit public mode: `Concept`, `Replay`, `Live`, or `Planned`;
6. a project-preparation contract describing required and optional inputs;
7. a reviewer or method-owner signoff before a public status upgrade.

## Runtime and Content State

| State | Meaning |
|---|---|
| `runtime=unavailable` | no verified complete-method execution is available in OpenDub |
| `runtime=experimental` | a real, constrained run exists but has not met stable release gates |
| `runtime=stable` | a verified complete-method adapter and regression record are released |
| `content=concept` | evidence-backed explanation only |
| `content=replay` | authorized recorded result with provenance |
| `content=live` | a new verified execution can be initiated locally |
| `content=planned` | future extension only |
