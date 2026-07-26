# Grant Positioning and Deliverables

## One Project, One Platform, One Repository

| Field | Locked value |
|---|---|
| Project name | **OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台** |
| English name | **OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing** |
| Product descriptor | Interactive Method Atlas, Visual Comparison, and Complete-Method Workbench |
| Main repository | `https://github.com/wsincos/OpenDub` |
| Application direction | AIGC 应用与工具 |
| Platform-code license | Apache-2.0 |

HPMDubbing, StyleDubber, and EmoDubber are the team's research foundations and first three complete platform methods. They are not three separate applications and are not fused into a new neural model.

## One-Sentence Summary

OpenDub is an open-source AIGC video-dubbing platform that uses an interactive visual Atlas to help creators and developers understand the multimodal task, select a complete method, prepare authorized local inputs, inspect evidence, and later compare or run verified methods through one reproducible workbench.

## Application Narrative

Video dubbing requires more than text-to-speech. A target video supplies lip movement, facial expression, scene, timing, and role context; target text supplies what must be spoken; authorized reference speech supplies permitted speaker identity or voice style. Existing research methods are often isolated as papers, separate codebases, and static examples. Their inputs, runtime conditions, evidence, and results are difficult to understand, select, reproduce, or compare.

OpenDub addresses this fragmentation as an AIGC tool platform. Its interactive Method Atlas is the normal user entry: users explore `Video + Text + Authorized Reference Speech -> one complete method -> Target Speech -> Dubbed Video`, inspect three complete research methods, select the method that matches a declared goal, and carry that selection into a local authorized project. The platform records source, license, rights, and status so a conceptual explanation is never mistaken for a recorded or fresh model result.

## New Open-Source Contribution

1. A task-first, interactive expression of multimodal video dubbing for creators, reviewers, and students.
2. A reusable, manifest-driven catalog of complete methods, including their input contracts, components, evidence, and project-preparation requirements.
3. A visual method-selection workspace linking explanation to an authorized local project workflow.
4. A consistent evidence protocol for `Concept`, `Replay`, `Live`, and `Planned` content.
5. A future-ready but bounded route from project preparation to authorized replay, fair comparison, and isolated complete-method execution.

## Required Grant-Release Deliverables

- Task Explorer and the three-method interactive Atlas.
- HPMDubbing, StyleDubber, and EmoDubber Method Canvases with method-specific interaction and evidence.
- method-selection handoff into Studio, retaining the selected complete method and declared input/control contract.
- local project preparation for authorized video, text, reference speech, timing, and rights.
- Evidence Room, model-status documentation, source/rights audit, and contribution entry point.
- architecture illustration, tests, quality record, release candidate, and an application demonstration video.

## Conditional Deliverables

| Capability | Condition |
|---|---|
| public Replay | authorized result bundle with hashes and provenance |
| A/B/C comparison | at least two qualified results produced from the same recorded input contract |
| Live generation | one complete method passes source, weight, rights, isolated-runtime, smoke-test, and run-manifest gates |
| automated orchestration / multilingual workflow | a separately tested future milestone |

These conditions are assets of the roadmap, not weaknesses of the first release. The project must never fabricate an output, metric, or Live label to satisfy them.

## Simple Milestone Plan

| Phase | Main deliverable | Grant relevance |
|---|---|---|
| P0 | current alpha and Concept Atlas foundation | demonstrated technical base |
| P1 | interactive Atlas as method-selection front door | visible product differentiation |
| P2 | selected method retained in an authorized local project | practical AIGC workflow |
| P3 | documentation, release record, architecture, and film | submission and open-source handoff |
| P4 | qualified Replay and comparison | evidence-gated enhancement |
| P5 | first verified Live method | evidence-gated enhancement |

## Suggested Funding Use

For a 12,000 RMB focus grant, prioritize interaction/product engineering, authorized demonstration assets, method/evidence review, documentation, quality assurance, and a controlled adapter/checkpoint audit. GPU inference receives a bounded verification allocation; it does not consume the release by forcing an unverified Live demonstration.

## Film Story

The film should demonstrate a platform, not a paper slideshow:

1. show why video dubbing is multimodal AIGC;
2. enter the Atlas and select a complete method;
3. interact with one distinctive method mechanism, then show the other two as a coherent method catalog;
4. open Evidence Room to demonstrate responsible, truthful open-source practice;
5. hand the selected method to a prepared local project;
6. state that Replay and Live appear only when qualifying evidence is present.

The detailed production pack remains in `DEMO_FILM/`. Its wording must use the official platform name above.
