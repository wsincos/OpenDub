# OpenDub Scope Lock and Product Decision

**Status:** locked for the first public Atlas release
**Applies to:** grant narrative, repository structure, UI, demo film, public claims and release review
**Change control:** changing this document requires an ADR and updates to the method manifests, test plan and demo script.

## 1. The project we are building

### Recommended application title

> **OpenDub: 面向视频配音生成的交互式方法图谱、可视化比较与开源复现平台**

English subtitle:

> **Interactive Atlas for Visual Dubbing Methods**

This framing is the strongest fit for the seed-grant application because it has one coherent problem, a bounded engineering deliverable and a clear connection to the team's original work. It does not present a collection of unrelated repositories as a project, and it does not claim a new hybrid neural network that has not been validated.

### What is genuinely new in OpenDub

The prior research contribution remains in the three complete methods. The new open-source contribution is the layer around them:

1. an accurate, interactive explanation of the video-dubbing task;
2. one inspectable visual representation for each *complete* method;
3. a common way to select, observe and later compare methods without altering their internals;
4. an evidence system that distinguishes paper-derived explanation, replayed outputs and actual local inference;
5. a recording-ready experience that makes the research contribution legible in minutes.

The platform is therefore an **interactive research instrument**, not a paper gallery and not a fourth model.

## 2. Locked method scope

Only the following three methods appear as first-class selectable methods in `v0.1.0-atlas`:

| Public label | Complete method | Research emphasis | Atlas visual signature |
|---|---|---|---|
| `HPMDubbing` | *Learning to Dub Movies via Hierarchical Prosody Models* (CVPR 2023) | Hierarchical Lip, Face and Scene cues for prosody | three visual layers converge into duration, pitch and energy |
| `StyleDubber` | *Towards Multi-Scale Style Learning for Movie Dubbing* (Findings of ACL 2024) | phoneme-level and utterance-level style learning | frame-scale versus phoneme-scale alignment |
| `EmoDubber` | *Towards High Quality and Emotion Controllable Movie Dubbing* (CVPR 2025) | synchronization, pronunciation and user-controllable emotion | positive/negative emotion guidance and intensity |

`HPMDubbing_Vocoder`, preprocessing code and media utilities are supporting infrastructure. They may appear in an evidence trail or an output-stage explanation but are never listed as a fourth peer method. All other GalaxyCong repositories remain outside the public method selector until they pass the complete-method admission gate.

### Non-negotiable boundary

```text
Allowed:
  viewer requirement -> choose one complete method -> inspect / replay / run that method

Forbidden:
  take an internal HPM module + an internal Style module + an internal Emo module
  -> present an unvalidated hybrid as OpenDub
```

The UI may compare research ideas across methods. It must not imply that their components have interchangeable checkpoints, feature spaces or training assumptions.

## 3. The task the first screen must explain

### Research formulation

```text
Inputs
  V      = silent target video
  X      = target text or subtitle
  A_ref  = authorized reference speech
  C      = optional method-specific control

Target dubbing speech
  A_hat = F_theta(V, X, A_ref, C)

Product rendering
  Y = Mux(V, A_hat)
```

### Human-readable formulation

```text
Video + Text + Reference Voice -> Dubbing Method -> Target Speech
                                                  -> Dubbed Video
```

The crucial distinction:

- `A_hat`, the target speech, is the research method's output.
- `Y`, the dubbed video, is an OpenDub product rendering produced by muxing the target speech with the target video.
- `C` is absent unless the selected method actually supports it. In the first release only EmoDubber exposes a user-facing emotion type and intensity control.

### What makes this different from ordinary TTS

The task must visibly establish four constraints before naming a model:

| Constraint | Question the viewer should understand | Visible evidence |
|---|---|---|
| lexical content | What is spoken? | text and phoneme sequence |
| timing and lip motion | When and at what rhythm is it spoken? | frame cursor, lip crop and duration/alignment |
| identity | Who is speaking? | authorized reference-speech segment |
| style and emotion | How should the line be delivered in this scene? | facial/scene cues or the supported user control |

## 4. Product experience: one guided line, five spaces

The default route is `/explore`. A reviewer should never land on an opaque architecture chart.

```text
1. Task Explorer
   understand the input constraints and two outputs
             |
             v
2. Method Atlas
   select one of three complete research methods
             |
             v
3. Method Canvas
   click its components and inspect its distinctive idea
             |
             v
4. Evidence / Comparison
   verify provenance; compare only when a common-input gate passes
             |
             v
5. Studio / Live (optional)
   run an admitted complete method locally and preserve a run record
```

### 4.1 Task Explorer: the 15-second explanation

The opening scene is a neutral, rights-cleared 8-12 second target clip. It builds the equation progressively:

1. **Video:** display a silent scene with a stable frame cursor.
2. **Text:** insert the target line, then show its phoneme representation.
3. **Reference voice:** add the authorized reference segment and its identity role.
4. **Visual cues:** expose Scene, Face and Lip overlays, one at a time.
5. **Method:** let the viewer choose HPMDubbing, StyleDubber or EmoDubber.
6. **Output:** keep separate tabs for `Target Speech` and `Dubbed Video`.

The product feel comes from a shared time cursor crossing all input and output modalities. It must never come from a decorative "AI brain" or an unlabelled synthetic waveform.

### 4.2 Method Atlas: choose a full method by research need

The selector is a research map, not a marketing scorecard:

| Viewer intent | Method that can be explored | Exact reason shown in UI |
|---|---|---|
| Understand how visual layers influence prosody | HPMDubbing | Lip, Face and Scene cues have separate prosodic roles |
| Understand why phoneme-scale alignment matters | StyleDubber | frame-level and phoneme-level views are compared explicitly |
| Explore an explicit emotion control | EmoDubber | emotion type and intensity are declared inputs |

No view says that one method is globally "best." Any quantitative comparison appears only after the common-input, common-preprocessing and rights gates pass.

### 4.3 Method Canvas: one visual language, three non-interchangeable stories

Every canvas has the same interaction grammar:

- click an architecture component to select it;
- select a component to highlight its actual upstream and downstream data relation;
- inspect its research question, typed inputs, typed outputs, paper anchor and content state;
- pin an available time-aligned signal to the signal dock;
- open the method's dedicated **Concept Lab** for its explanatory interaction;
- follow an evidence link before treating a signal as a real run artifact.

It deliberately does **not** render every neural layer. A node exists only if it represents a paper-defined component or a meaningful stage of the complete method.

#### HPMDubbing Concept Lab: Hierarchical Prosody Lens

```text
Lip motion   -> duration / local timing
Face affect  -> pitch + energy / local expression
Scene affect -> global emotion / utterance context
                         \  |  /
                          Hierarchical prosody
                                  |
                            mel -> waveform
```

- Three selectable layers have distinct colors and frame crops.
- Selecting a layer changes the highlighted relationship and written explanation.
- The same time cursor can later synchronize Lip ROI, Face ROI, phonemes, duration, F0 and energy.
- In Concept mode the curves are illustrative and visibly labelled as such; they are never scored as model output.

#### StyleDubber Concept Lab: Multi-scale Alignment Lens

```text
frame sequence:      [ f0 ][ f1 ][ f2 ][ f3 ][ f4 ][ f5 ]
phoneme intervals:   [       p0       ][    p1    ][ p2 ]
                           local              utterance-level style
```

- A segmented control switches between **Frame scale** and **Phoneme scale**.
- The selected phoneme interval highlights its contributing frame group, reference-speech range and corresponding generated-speech range when replay data exists.
- MPA, PLA and USL remain three named method components; they are not renamed into generic "style modules."
- In Concept mode the alignment is an explanatory interval map, not a falsely claimed attention map.

#### EmoDubber Concept Lab: Emotion Guidance Lens

```text
reference identity + synchronized phoneme sequence + requested emotion
                                                    |
                               positive guidance --+-- negative guidance
                                                    |
                                            controllable target speech
```

- Emotion type uses an explicit segmented control; intensity uses a labelled range control.
- Changing either control updates only the conceptual guidance diagram unless an exact authorized Replay result or an admitted Live run exists.
- The page explicitly says that Concept mode has generated no new audio.
- The interaction presents the distinct positive/negative guidance idea without inventing latent trajectories or fake audio controls.

### 4.4 Evidence Room: the credibility layer

Each method must expose the following facts in one compact, readable row:

```text
Paper -> source repository -> pinned source commit -> code license
      -> weight terms -> content mode -> runtime status -> last verification
```

This room is mandatory for the grant story. It turns the platform from a visually polished demo into an inspectable open-source deliverable.

### 4.5 Comparison and Live are gates, not visual promises

| Capability | May be shown when | Required on-screen label |
|---|---|---|
| Concept explanation | component and relation were reviewed against primary sources | `Concept` / `Illustrative` where appropriate |
| Replay audio or signal | source, method revision, file hash and display/distribution rights are recorded | `Replay` |
| common-input method comparison | two or more results have equal video, text, reference-audio, crop and preprocessing identities | `Replay comparison` or `Live comparison` |
| changed-input inference | fixed code revision, explicit weight terms, weight hash, authorized input and successful isolated smoke run exist | `Live` |

Failure to pass a gate is a valid, polished state: the page describes what evidence is missing and keeps the task and method visualizations usable.

## 5. Visual and interaction direction

### Design thesis

> **Editorial Research Instrument with cinematic post-production precision.**

The application should look like a purpose-built research console, not a SaaS dashboard and not an AI landing page.

- Main material: real scene frames, lip/face crops, phoneme intervals, prosody plots, spectrograms and waveforms.
- Main geometry: a flat neutral canvas, precise dividers, stable grid alignment, small-radius instruments and compact labels.
- Motion: follows causality and time. Edges highlight because a user selects a component; playheads move because time advances.
- Color: only marks modality and state. Video blue, text violet, voice teal, prosody amber, emotion rose and output green are never used as full-page gradients.
- Typography: readable Chinese body text plus compact monospaced values, with no viewport-scaled type or negative letter spacing.

### Explicitly reject

- a landing-page hero that hides the product;
- generic cards full of model names and badges;
- fake live inference, fake audio playback or randomly animated waveforms;
- paper screenshots used as a substitute for an interactive explanation;
- dramatic claims such as "best", "perfect sync", "real-time" or "one click" without attached evidence.

## 6. Release hierarchy and success evidence

### Release 0: recording-ready Concept Atlas

Required before a professional product video is recorded:

- Task Explorer communicates `Video + Text + Reference Voice -> Target Speech`.
- All three method pages have their complete semantic graph, unique Concept Lab and source links.
- Every conceptual view is visibly labelled and keyboard operable.
- Evidence Room declares current code/weight/content status.
- No stale route, unfinished placeholder or fictitious result is visible in the recording path.
- Desktop `1920x1080` and `1440x900`, plus mobile `390x844`, have been visually inspected.

### Release 1: evidence-backed Replay comparison

Required before audio A/B/C or metric claims are shown publicly:

- at least two methods have authorized outputs for one exactly identical input package;
- all media, metadata and hashes pass validation;
- synchronized playback is mutually exclusive;
- any metric includes unit, preprocessing and applicability;
- the recording script is revised so every result is called `Replay`, not `Live`.

### Release 2: one admitted Live method

Required before a live-generation interaction is recorded:

- a single full method passes the code, weights, rights and smoke-test gate;
- the generated target speech and selected genuine intermediate artifacts are stored in a run manifest;
- failure states do not contaminate the Atlas;
- the film says exactly which method and environment produced the run.

## 7. One-minute reviewer outcome

After one minute, a grant reviewer should be able to say:

1. "This is video dubbing, not generic TTS: it uses video, text and a reference voice."
2. "The team already has three distinct, complete methods with a visible research progression."
3. "OpenDub makes their mechanisms, evidence and future comparison understandable instead of merely listing papers."
4. "The current status is honest: explanation, replay and live generation are clearly separated."

That outcome, rather than a large count of repositories or a speculative hybrid model, is the project's central advantage.
