# OpenDub Project Charter

## Mission

OpenDub is an open-source platform for multimodal intelligent video dubbing in AIGC content creation. It makes complete video-dubbing methods understandable, selectable, inspectable, reproducible, and, when verification permits, locally runnable.

The platform's defining public experience is not a generic model dashboard. It is an interactive visual workbench where a user can see how video, text, and authorized reference speech become target dubbing speech through one complete method.

## Problem

Video dubbing is constrained by video timing, lip movement, facial expression, scene context, target text, speaker identity, and desired style or emotion. Existing work is often released as a paper, an isolated training repository, and a static demonstration. This leaves three gaps:

1. Creators cannot easily determine which complete method fits their stated need.
2. Students and reviewers cannot trace a method from multimodal inputs through its own components to output.
3. Developers cannot fairly compare or reproduce methods when inputs, source revisions, rights, checkpoints, and output evidence are fragmented.

## Product Promise

```text
Video + Target Text + Authorized Reference Speech
                    -> select one complete dubbing method
                    -> Target Dubbed Speech
                    -> muxed Dubbed Video
```

OpenDub provides the surrounding product and evidence layer. It does not claim to alter the scientific internals of HPMDubbing, StyleDubber, or EmoDubber.

## Primary Users

| User | Main outcome |
|---|---|
| AIGC content creator | understand the requirements and constraints of a dubbing task; prepare an authorized local project; select a suitable complete method |
| reviewer, teacher, or student | understand the task and inspect the evidence-backed mechanism of each method in minutes |
| method developer | publish a complete method through a documented manifest, evidence record, replay package, and optional isolated adapter |

## Product Pillars

1. **Interactive visualization is the front door.** Task Explorer, Atlas, Canvas, and signal views are the normal way users enter and operate the platform.
2. **Complete methods are selected, not spliced.** The method selector compares declared properties of independent end-to-end methods.
3. **The Studio turns selection into a project.** It records authorized media, script, reference speech, timing, and selected-method requirements.
4. **Evidence precedes a claim.** Paper, source, license, checkpoint, rights, result, and runtime state are visible and independently recorded.
5. **AIGC use is local-first and responsible.** The platform requires owned or authorized inputs and avoids claiming unrestricted voice cloning or arbitrary media use.

## Application Value

For the seed grant, the project delivers an open, reusable AIGC tool rather than another single-paper repository:

- a task-first education and decision interface for multimodal video dubbing;
- a reusable manifest and evidence model for complete methods;
- an interactive workspace that links method understanding to project preparation;
- a foundation for later replay, comparison, local inference, and third-party method contribution.

## Non-Goals for the First Application Release

- training a new hybrid network;
- claiming live generation for unverified public checkpoints;
- promising multilingual, multi-character, or agentic automation before it is tested;
- integrating unrelated repositories merely to increase the project count;
- publishing copyrighted video, unconsented voice, or result media without distribution rights.

## Release Logic

The required release is a polished `Concept` platform with three complete method experiences and a usable local project-preparation path. `Replay`, same-input comparison, and `Live` execution are additive phases with explicit gates. A blocked checkpoint never invalidates the initial platform release.
