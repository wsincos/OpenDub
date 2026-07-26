# OpenDub From-Zero Launch Playbook

Use this document when the instruction is “start implementation.” The immediate goal is not to rebuild a video-dubbing model. It is to advance the current alpha toward the application-first platform path defined in [PLATFORM_POSITIONING.md](../00_PRODUCT/PLATFORM_POSITIONING.md).

## 1. Read in This Order

1. [Platform positioning](../00_PRODUCT/PLATFORM_POSITIONING.md)
2. [Scope lock](../00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md)
3. [Current status](STATUS.md)
4. [Application-first implementation plan](IMPLEMENTATION_PLAN.md)
5. [Complete-method catalog](../01_CAPABILITIES/CAPABILITY_AND_MODEL_MAP.md)
6. [Platform architecture](../02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
7. [Quality plan](QUALITY_PLAN.md)

## 2. Establish the Baseline

Run the repository's current quality gate before editing:

```bash
make check
uv run python scripts/verify_registry.py model-registry/upstreams.yaml
```

Then inspect the worktree, current routes, and current status. Do not overwrite user media, `reference/`, checkpoints, private project data, or unrelated changes.

## 3. Choose the First Unfinished Phase

| Status finding | Start here |
|---|---|
| catalog or selection handoff is missing | P1 in `IMPLEMENTATION_PLAN.md` (already implemented; investigate a regression) |
| selected method is not retained by Studio | P2 (already implemented; investigate a regression) |
| application docs, film, release record, or visual QA is incomplete | P3 |
| qualified same-input result bundles exist | P4 |
| one method satisfies the full admission gate | P5 |

Do not jump to P4 or P5 merely because a checkpoint file or online demo can be found.

## 4. Vertical-Slice Discipline

For every change:

1. write the failing unit, integration, or component test;
2. run it and confirm the intended failure;
3. implement the smallest behavior;
4. run focused tests, the full quality gate, and the relevant production build;
5. inspect desktop and mobile routes when the UI changes;
6. update `STATUS.md` with evidence and make an intentional commit.

## 5. Non-Negotiable Truth Rules

- `Concept` changes explanation only.
- `Replay` chooses a qualified existing result only.
- `Live` requires a completed verified run record.
- no unavailable signal is replaced by a random wave, metric, or neural animation.
- selection compares complete methods; it never connects their internal modules.
- all video, scripts, and reference speech are owned or authorized.

## 6. Definition of a Good P0-P3 Release

The release is ready for the application when an evaluator can follow this path without external services: understand the task, inspect and select one of three complete methods, see its evidence and limitations, prepare an authorized local project, and understand precisely why Replay or Live is or is not available.
