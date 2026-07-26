# OpenDub Planning Hub

This directory is the planning source for one grant project and one repository:

> **OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台**
>
> *OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing*

OpenDub is a platform, not a fourth dubbing model. Its flagship experience is an **interactive Method Atlas** that people use to understand the task, inspect complete methods, choose a method for a declared need, prepare an authorized project, and later inspect valid Replay or Live results in the same workspace.

## Read This First

1. [Platform positioning and application strategy](00_PRODUCT/PLATFORM_POSITIONING.md)
2. [Project charter](00_PRODUCT/PROJECT_CHARTER.md)
3. [Scope lock and release boundary](00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md)
4. [Current implementation status](03_EXECUTION/STATUS.md)
5. [From-zero launch playbook](03_EXECUTION/START_HERE.md)

These five documents override earlier detailed planning documents when wording conflicts. The remaining files are implementation, evidence, film, and governance appendices.

## Locked Product Line

```text
Understand and select
  Task Explorer -> Method Atlas -> Method Canvas -> Evidence-aware choice

Prepare and use
  Studio -> authorized video / text / reference speech -> selected complete method
         -> Concept, Replay, or verified Live -> compare / export / reproduce
```

The visual and interactive experience is the main entry point and the primary public demonstration. Studio and adapters make the experience useful for AIGC video-content workflows when evidence admits them.

## Core Method Scope

| Method | Platform purpose | First-release status |
|---|---|---|
| HPMDubbing | inspect and select hierarchical visual prosody | Concept |
| StyleDubber | inspect and select multi-scale style learning | Concept |
| EmoDubber | inspect and select emotion-guided dubbing | Concept |

They remain independent complete methods. OpenDub standardizes the surrounding project, selection, evidence, replay, and adapter contracts; it must not splice their internals into an unverified hybrid.

## Application-First Release Boundary

### Required

- Task Explorer, Method Atlas, three Method Canvases, Evidence Room, and a credible recording route.
- A local project path for authorized video, text, reference speech, timing, and selected-method requirements.
- Structured manifests, source/rights evidence, documentation, CI, and a release candidate.

### Conditional

- Replay audio/video only with an authorized result bundle.
- A/B/C comparison only with same-input qualified results.
- Live generation only after a complete method passes the admission gate.

Do not delay the application release for a checkpoint. Do not substitute fabricated media, metrics, or model behavior for a blocked conditional item.

## Roadmap

| Phase | Outcome | Checkpoint required? |
|---|---|---:|
| P0 | current alpha foundation and three-method Concept Atlas | no |
| P1 | Atlas becomes the platform's method-selection front door | no | completed in the current application-release working tree |
| P2 | Studio records authorized inputs and the selected complete-method contract | no | completed in the current application-release working tree |
| P3 | grant release: documentation, evidence, quality record, and film | no | documentation, architecture, and QA are in final freeze; recording follows the prepared script |
| P4 | qualified Replay and fair comparison | no, but authorized outputs are required |
| P5 | first admitted Live method | yes |

P0-P3 are the simple, most appropriate seed-grant scope. P4 and P5 are evidence-gated platform growth, not application-release promises.

## Document Map

### Product

- [Platform positioning](00_PRODUCT/PLATFORM_POSITIONING.md)
- [Task definition](00_PRODUCT/TASK_DEFINITION.md)
- [Product experience](00_PRODUCT/PRODUCT_EXPERIENCE.md)
- [User workflows](00_PRODUCT/USER_WORKFLOWS.md)
- [Scope and success criteria](00_PRODUCT/SCOPE_AND_SUCCESS.md)

### Complete methods and evidence

- [Method selection map](01_CAPABILITIES/CAPABILITY_AND_MODEL_MAP.md)
- [Three-method interaction specification](01_CAPABILITIES/METHOD_EXPERIENCE_SPEC.md)
- [Visualization signal map](01_CAPABILITIES/VISUALIZATION_SIGNAL_MAP.md)
- [Upstream baseline](01_CAPABILITIES/UPSTREAM_BASELINE.md)

### Architecture and execution

- [Platform architecture](02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
- [Atlas contracts](02_ARCHITECTURE/ATLAS_CONTRACTS.md)
- [Implementation plan](03_EXECUTION/IMPLEMENTATION_PLAN.md)
- [Quality plan](03_EXECUTION/QUALITY_PLAN.md)

### Application and governance

- [Grant positioning and deliverables](04_OPEN_SOURCE/GRANT_AND_DEMO.md)
- [Film production pack](04_OPEN_SOURCE/DEMO_FILM/README.md)
- [Decisions and gates](05_GOVERNANCE/DECISIONS_AND_RISKS.md)
- [Definition of done](05_GOVERNANCE/DEFINITION_OF_DONE.md)

## Implementation Rule

When instructed to implement, begin with the first unfinished phase in [STATUS.md](03_EXECUTION/STATUS.md). P1 and P2 are complete unless a regression is found. Keep all changes tied to the locked product line above, update the evidence record with each claim, and preserve the `Concept` / `Replay` / `Live` distinction.
