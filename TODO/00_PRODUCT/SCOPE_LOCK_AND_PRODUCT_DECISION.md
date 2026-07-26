# Scope Lock and Product Decision

**Status:** locked for the seed-grant application release

**Authority:** [Platform Positioning](PLATFORM_POSITIONING.md)

## The Decision

OpenDub will be built and presented as an **AIGC video-dubbing platform**. Its core public product is the interactive Method Atlas and visual workbench; its practical project path is Studio-based preparation of authorized inputs for one selected complete method.

The first application release is deliberately bounded. It does not need a new training run or a publicly usable checkpoint to be valuable, testable, and recordable.

## Required First-Release Product Path

```text
1. Understand the task
   Video + Text + Authorized Reference Speech -> Target Speech -> Dubbed Video

2. Explore and select a complete method
   HPMDubbing / StyleDubber / EmoDubber

3. Inspect method constraints and evidence
   inputs, controls, source, license, weight/runtime status

4. Prepare an authorized local project
   video, script, reference voice, timing, rights, selected method

5. Inspect an admitted outcome when available
   Concept explanation / Replay result / verified Live run
```

## Core Methods

Only HPMDubbing, StyleDubber, and EmoDubber are first-class selectable methods. Each remains an independent complete method.

| Method | Selection message |
|---|---|
| HPMDubbing | choose when hierarchical Lip, Face, and Scene cues are the central explanatory focus |
| StyleDubber | choose when multi-scale, phoneme- and utterance-level style is the central explanatory focus |
| EmoDubber | choose when an explicit emotion category and intensity control is the central explanatory focus |

The selector gives an evidence-bound recommendation, never an unconditional statement that one method is globally best.

## Explicitly Forbidden

```text
HPMDubbing internal module + StyleDubber internal module + EmoDubber internal module
    -> described as a new OpenDub model
```

Also forbidden: calling Concept animation an output, calling a prerecorded file `Live`, claiming a model is available solely because a paper or download link exists, or using unauthorized identity/audio/video material.

## Release Tiers

| Tier | User-visible capability | Admission rule |
|---|---|---|
| Concept | interactive explanation, method selection, component and signal interpretation | primary-paper and fixed-source evidence |
| Replay | authorized historical result and its provenance | rights, hashes, source/result record, reviewer approval |
| Live | a new local output from one complete method | source, code license, weight terms/hash, authorized smoke input, isolated runtime, run manifest |
| Planned | a visible future route | no operational claim |

## What Is Required Before Submission

- three accurate and usable Concept Method Canvases;
- a method-selection handoff into the local project workflow;
- Evidence Room and clear status labels;
- documentation, tests, release record, and a recorded walkthrough;
- grant prose that states the platform and its user value clearly.

Replay, a fair multi-method comparison, and a verified Live run improve the application but are not mandatory. They must not be substituted with fabricated assets if their admission gates remain closed.

## Change Control

Any change to the three-method core, the first-release boundary, or the status definitions requires an entry in `05_GOVERNANCE/DECISIONS_AND_RISKS.md`, a corresponding update to this file, and a review of the grant narrative and film script.
