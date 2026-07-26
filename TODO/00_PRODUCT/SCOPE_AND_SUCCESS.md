# Application Release Scope and Success Criteria

This document defines the smallest release that is both strong for the grant application and realistic with the project's verified current state.

## Required Scope: P0-P3

### P0: existing foundation

- local project, media, authorization, timeline, API, CLI, and Studio foundation;
- the three-method Concept Atlas, Method Canvas interactions, Evidence Room, and evidence-gated comparison route;
- automated tests, content validation, production build, and current-source audit.

### P1: Atlas as the platform front door

- the first route teaches the task in 15 seconds: `Video + Text + Authorized Reference Speech -> one complete method -> Target Speech -> Dubbed Video`;
- three complete methods can be explored, compared by declared capability, and selected without implying a hybrid model;
- every method view exposes components, visual explanations, source links, evidence state, and input/control requirements;
- choosing a method produces a handoff record that Studio can understand.

### P2: usable project preparation

- a creator can create a local project, add owned or authorized video, text, reference speech, time window, and rights record;
- the selected method and its required/optional controls are retained in the project manifest;
- unavailable runtime states are understandable and do not erase a prepared project;
- the project can be exported as a reproducibility record even when no Live adapter is available.

### P3: grant release package

- an application-oriented README, quick start, model-status page, architecture diagram, and contribution entry point;
- a reproducible screen-recording route through Task Explorer, selection, one method interaction, Evidence Room, and project handoff;
- a release candidate with a fixed commit, passing checks, known limitations, and a claim-evidence index;
- a completed application form and film whose statements match the release state.

## Conditional Scope: P4-P5

| Phase | Outcome | Gate |
|---|---|---|
| P4 | authorized Replay and same-input comparison | qualifying result bundles from at least two methods |
| P5 | first new Live output | complete-method admission gate, including rights, terms, hash, isolated smoke test, and run manifest |

## Explicitly Deferred

- a new model trained from the three methods;
- automatic plot analysis, translation, character assignment, or agentic pipeline orchestration;
- multilingual, multi-character, real-time, production-scale, and national-GPU claims;
- public model-weight redistribution;
- global rankings between methods.

## Acceptance Criteria

### User value

- A reviewer can explain why the task is not generic TTS after visiting the first route.
- A creator can select a method based on a stated need and see the selection reflected in a local project.
- A developer can locate the paper, fixed source, license, runtime state, and extension requirements for each method.

### Visual and interaction quality

- Task Explorer, Atlas, all three method pages, Evidence Room, and Studio handoff are usable at `1440x900`, `1920x1080`, `1280x720`, `768x1024`, and `390x844`.
- Graph nodes are keyboard-accessible buttons; controls have explicit labels; no status depends only on color.
- The page never uses decorative moving signals to represent unavailable model output.

### Truth and reproducibility

- every public method claim maps to a paper, fixed upstream source, or tested implementation record;
- Concept, Replay, Live, and Planned content are visibly and consistently labelled;
- public assets record origin and permissions; reference speech requires authorization;
- selected-method, input, and project revision information are retained in exported project or run records.

### Engineering quality

- the existing project checks, manifest validation, frontend type/build checks, and documentation-link checks pass;
- the release candidate is tied to a commit, version, screen-recording log, and known-limitations record;
- no user media, unverified checkpoint, credentials, or private local path enters the public repository.

## Success Definition

The application release succeeds when the repository is a credible, usable open-source entry point for AIGC video dubbing: people can learn the task, inspect and select a complete method, prepare an authorized project, understand what is and is not runnable, and see a clear path to replay or local execution. A missing checkpoint may block P4/P5; it does not invalidate P0-P3.
