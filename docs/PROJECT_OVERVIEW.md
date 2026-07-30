# OpenDub Project Overview

> **OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing**
> **OpenDub：多模态智能视频配音开源平台**

OpenDub is a local-first platform for understanding and preparing the
multimodal video-dubbing task. It brings together the team's complete research
methods, authorized archived examples, interactive visual explanation, and
evidence-aware project preparation in a single open-source experience.

## Task Statement

```text
Video + Text + Authorized Reference Speech
              -> one complete dubbing method
              -> Target Dubbed Speech + Dubbed Video
```

The video provides visual timing and context; text defines the intended line;
authorized reference speech supplies the permitted identity and style condition.
The platform makes each of these roles observable before a user selects or
prepares a complete method.

## What OpenDub Provides

1. **Task Stage**: an interactive explanation of video, text, reference speech,
   synchronized timing, target speech, and dubbed-video outputs.
2. **Method Atlas**: original-paper architecture views and clickable component
   explanations for HPMDubbing, StyleDubber, and EmoDubber.
3. **Archived Examples and Compare**: authorized historical media shown with
   derived waveform, log-mel, F0, energy, and frame-contact evidence.
4. **Evidence and Studio**: source/rights records, complete-method selection,
   authorized local inputs, and a versioned preparation export.

## Complete-Method Boundary

OpenDub does not construct a new neural network by combining modules from
different papers. Each team-developed method remains complete and independent:

| Method | Primary emphasis |
| --- | --- |
| HPMDubbing | Visual prosody across lip, face, and scene cues |
| StyleDubber | Multi-scale pronunciation and character style |
| EmoDubber | Synchronization, identity, pronunciation, and controllable emotion |

The interactive pages explain these methods and retain evidence for their source
records. They do not turn a concept diagram into a model-output claim.

## Evidence Boundary

The public experience includes interactive explanation, method inspection,
authorized archived research examples, and local project preparation. It does
not claim fresh OpenDub inference, a fair cross-method ranking, or a verified
live runtime until the relevant method has a pinned source revision, licensed
weights, an isolated runtime, authorized fixtures, and a real smoke test.

## Explore

- [Watch the final project film](showcase/README.md)
- [Run the local web experience](getting-started/local.md)
- [Inspect the platform architecture](architecture/README.md)
- [Read method admission status](adapters/model-status.md)
- [Review public example-media authorization](rights/showcase-media-rights-v3.md)
