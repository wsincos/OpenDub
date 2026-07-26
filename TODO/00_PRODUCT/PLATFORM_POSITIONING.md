# OpenDub Platform Positioning and Application Strategy

**Status:** binding for the seed-grant application and the next implementation cycle
**Last revised:** 2026-07-26
**Supersedes on conflict:** earlier wording that presents OpenDub primarily as a standalone “Method Atlas” or as a model-integration project.

## 1. Official identity

### Chinese application name

> **OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台**

### English name

> **OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing**

### Product descriptor

> **Interactive Method Atlas, Visual Comparison, and Complete-Method Workbench**

The application name states the user-facing AIGC value. The descriptor states the differentiating product mechanism. They are not competing names and should be used together where space permits.

## 2. One-sentence application statement

OpenDub is an open-source platform for AIGC video-content creation that helps users understand video dubbing, select an appropriate complete dubbing method, prepare authorized inputs, inspect method evidence, compare valid results, and, only when verified assets are available, run that complete method locally.

## 3. The product is neither extreme

OpenDub is **not** any of the following:

- a fourth neural dubbing model;
- a collection page that merely links to paper repositories;
- a hybrid made by taking internal modules from HPMDubbing, StyleDubber, and EmoDubber;
- a promise that every listed method can already run with a public checkpoint;
- a voice-cloning service for unapproved identities.

OpenDub **is** a platform with two connected product loops:

```text
Understand and choose
  Task Explorer -> Method Atlas -> Method Canvas -> Evidence-aware selection

Prepare, inspect, and use
  Studio -> authorized project inputs -> Replay or verified Live run
         -> comparison / export / reproducibility record
```

The first loop is the signature user experience and remains useful without a GPU or checkpoint. The second loop turns the platform into an AIGC tool as evidence and complete-method adapters become available.

## 4. Why interactive visualization is the core feature

The interactive Atlas is not a decorative introduction or a one-off grant video. It is the platform's primary operating surface:

1. It explains why video dubbing requires **Video + Target Text + Authorized Reference Speech**, rather than text alone.
2. It lets a user choose among complete methods by stated need, such as hierarchical visual prosody, multi-scale style, or explicit emotion control.
3. It exposes inputs, expected controls, components, evidence, known constraints, and runtime status before a user attempts a run.
4. It gives developers a stable, manifest-driven place to register an additional complete method later.
5. It gives reviewers and creators one truthful place to distinguish `Concept`, `Replay`, `Live`, and `Planned` content.

The visual language therefore has an operational role: **understand -> select -> prepare -> inspect -> compare -> run when admitted**.

## 5. Core methods and their platform roles

| Complete method | Platform role | What the Atlas helps a user understand or select | Current public content mode |
|---|---|---|---|
| HPMDubbing | visual-prosody method | how Lip, Face, and Scene cues constrain duration, pitch, energy, and global affect | Concept |
| StyleDubber | multi-scale style method | how frame-, phoneme-, and utterance-level representations describe speaking style | Concept |
| EmoDubber | emotion-guided method | how synchronization, pronunciation, identity, and controllable emotion are represented | Concept |

`HPMDubbing_Vocoder`, preprocessing utilities, evaluation scripts, and media tools are supporting infrastructure. `LLM-Flow-Dubber` is a future intelligent-orchestration direction. None becomes a fourth peer method or an already available end-to-end platform feature without passing the complete-method admission gate.

## 6. Simple grant-first scope

The first application release must be credible and independently useful without waiting for an unverified checkpoint.

### Required for the application release

- a polished Task Explorer that explains the multimodal dubbing task and the difference between generated speech and a muxed dubbed video;
- a three-method interactive Atlas, with complete method paths, clickable components, method-specific visual explanations, and evidence links;
- a method-selection handoff that records the selected complete method and its declared input/control requirements in a local project;
- a local project preparation path for video, text, authorized reference speech, timing, and rights records;
- Evidence Room, model-status display, documentation, tests, and a recording-ready demonstration route;
- a release candidate and an honest grant film based on the verified Concept experience.

### Conditional upgrades, never blockers for the application release

- `Replay`: one or more authorized, hash-recorded historical outputs;
- same-input multi-method comparison: only after at least two qualifying Replay bundles exist;
- `Live`: one complete method after source, weights, rights, hash, isolated environment, and real smoke-test gates pass;
- agentic orchestration, multilingual workflows, multi-character automation, GPU portability, and industrial deployment.

## 7. Truth and safety rules

```text
Concept = paper/code-grounded explanation; no new model output is claimed.
Replay  = an existing authorized result bundle; it is never labelled as a fresh OpenDub run.
Live    = a verified complete-method run with a complete run manifest.
Planned = a visible roadmap item, not a disabled feature pretending to work.
```

All projects use owned or authorized video, text, and reference speech. OpenDub records that authorization before a reference voice can be used in a run or public replay package.

## 8. Reviewer outcome

Within one minute, a reviewer should understand:

1. Video dubbing is a multimodal AIGC task, not generic text-to-speech.
2. The team has three related, complete research methods with distinct contributions.
3. OpenDub makes those methods selectable, understandable, inspectable, and eventually comparable or runnable through one open platform.
4. The application does not overclaim unavailable checkpoints, fabricated outputs, or an unverified hybrid model.

## 9. Planning consequence

All future TODO items must answer one of these questions:

- Does this improve the Atlas as a method-selection and explanation workspace?
- Does this make authorized project preparation or complete-method use more reliable?
- Does this improve evidence, reproducibility, developer extension, or AIGC content-creation value?

If the answer is no, the item is out of the first application scope.
