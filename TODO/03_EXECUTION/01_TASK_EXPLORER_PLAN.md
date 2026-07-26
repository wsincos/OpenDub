# Task Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建无需 API 和 GPU 即可准确解释 Video + Text + Reference Speech 到 Dubbed Speech 的交互式首屏。

**Architecture:** Python/Pydantic 定义并校验 Atlas 内容契约，Vite 在构建时生成类型化内容索引；React Router 提供独立路由；TimelineController 将视频、文本、参考语音和输出绑定到整数微秒时间轴。

**Tech Stack:** Pydantic v2、Typer、JSON Schema、React 19、React Router、Zustand、Canvas、Vitest、Testing Library、Playwright。

## Global Constraints

- 默认入口是 `/explore`，不是项目列表。
- 研究输出为 Generated Speech，Dubbed Video 是 OpenDub 混流后的产品输出。
- Task Explorer 不依赖后端健康状态。
- 三项必需输入始终可见；方法特定控制按 manifest 显示。
- 自动导览在用户第一次交互后永久停止，页面刷新后可重新开始。
- 所有时间字段是整数微秒。
- 所有示意信号显示 `Illustrative`。

---

### Task 1: Atlas Content Models and Validation

**Files:**

- Create: `src/opendub/atlas/__init__.py`
- Create: `src/opendub/atlas/models.py`
- Create: `src/opendub/atlas/validation.py`
- Create: `src/opendub/atlas/hashing.py`
- Create: `schemas/method-v1.json`
- Create: `schemas/atlas-index-v1.json`
- Create: `schemas/case-v1.json`
- Create: `schemas/replay-v1.json`
- Create: `schemas/signals-v1.json`
- Create: `tests/fixtures/atlas/minimal/`
- Test: `tests/unit/atlas/test_validation.py`
- Modify: `scripts/export_schemas.py`

**Interfaces:**

- Produces: `MethodManifestModel`、`CaseManifestModel`、`ReplayBundleModel`、`validate_content(root: Path) -> ValidationReport`。
- Produces: five JSON Schemas matching [ATLAS_CONTRACTS.md](../02_ARCHITECTURE/ATLAS_CONTRACTS.md).

- [ ] **Step 1: Add failing graph and provenance tests**

```python
def test_method_rejects_edge_to_missing_node(minimal_method):
    minimal_method["graph"]["edges"][0]["target"] = "missing"
    report = validate_method(minimal_method)
    assert report.error_codes == ("ATLAS_EDGE_TARGET_MISSING",)

def test_replay_rejects_illustrative_numeric_signal(minimal_replay):
    minimal_replay["signals"][0] |= {"mode": "replay", "illustrative": True}
    report = validate_replay(minimal_replay)
    assert "ATLAS_REPLAY_ILLUSTRATIVE" in report.error_codes
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_validation.py -v`
Expected: collection fails because `opendub.atlas` does not exist.

- [ ] **Step 3: Implement Pydantic models and semantic validation**

Implement exact status literals, node/edge referential checks, POSIX relative asset paths, SHA-256 format, positive duration, rights gates and signal time binding. `ValidationReport` contains ordered `ValidationIssue(code, path, message)`.

- [ ] **Step 4: Export and round-trip schemas**

Add the Atlas models to `scripts/export_schemas.py`; validate the minimal fixtures with both Pydantic and `jsonschema`.

- [ ] **Step 5: Run validation tests**

Run: `uv run pytest tests/unit/atlas tests/unit/schemas -v`
Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add src/opendub/atlas schemas scripts/export_schemas.py tests/fixtures/atlas tests/unit/atlas
git commit -m "feat(atlas): define versioned content contracts"
```

### Task 2: Atlas CLI and Static Content Index

**Files:**

- Create: `src/opendub/atlas/cli.py`
- Create: `src/opendub/atlas/index.py`
- Create: `content/index.json`
- Create: `content/methods/.gitkeep`
- Create: `content/cases/.gitkeep`
- Create: `content/replays/.gitkeep`
- Test: `tests/unit/atlas/test_cli.py`
- Modify: `src/opendub/cli/app.py`
- Modify: `Makefile`

**Interfaces:**

- Produces: `opendub atlas validate CONTENT_ROOT`.
- Produces: `build_content_index(root: Path) -> AtlasIndexModel`.

- [ ] **Step 1: Write CLI exit-code tests**

```python
def test_atlas_validate_returns_two_for_invalid_content(runner, invalid_root):
    result = runner.invoke(app, ["atlas", "validate", str(invalid_root)])
    assert result.exit_code == 2
    assert "ATLAS_EDGE_TARGET_MISSING" in result.stdout
```

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_cli.py -v`
Expected: command `atlas` is not registered.

- [ ] **Step 3: Implement CLI and deterministic index**

Sort methods and cases by explicit `order`; write index using UTF-8, two-space indentation and newline termination. Validation exits `0` for valid content and `2` for content errors.

- [ ] **Step 4: Add content validation to repository checks**

Add `uv run opendub atlas validate content` after Schema checks in `make check`.

- [ ] **Step 5: Verify**

Run: `uv run pytest tests/unit/atlas/test_cli.py -v && uv run opendub atlas validate content`
Expected: pass with an empty but valid index.

- [ ] **Step 6: Commit**

```bash
git add src/opendub/atlas src/opendub/cli/app.py content Makefile tests/unit/atlas/test_cli.py
git commit -m "feat(atlas): add content validation command"
```

### Task 3: Web Test Harness, Router and App Shell

**Files:**

- Create: `apps/web/src/app/App.tsx`
- Create: `apps/web/src/app/AppRouter.tsx`
- Create: `apps/web/src/app/AppShell.tsx`
- Create: `apps/web/src/app/routes.ts`
- Create: `apps/web/src/app/NotFoundPage.tsx`
- Create: `apps/web/src/test/setup.ts`
- Create: `apps/web/src/app/AppRouter.test.tsx`
- Modify: `apps/web/src/main.tsx`
- Modify: `apps/web/package.json`
- Modify: `apps/web/vite.config.ts`
- Move: `apps/web/src/app/StudioApp.tsx` to `apps/web/src/features/studio/StudioApp.tsx`
- Move: `apps/web/src/app/shell/` to `apps/web/src/features/studio/shell/`

**Interfaces:**

- Produces: `createAppRouter()` and routes `/explore`, `/methods`, `/compare/:caseId`, `/studio`, `/evidence`.
- Consumes: existing `StudioApp` without behavior changes.

- [ ] **Step 1: Add dependencies and a failing route test**

Add exact dependencies: `react-router-dom`, `zustand`, `vitest`, `jsdom`, `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`.

```tsx
it("opens Task Explorer at the root route", async () => {
  render(<RouterProvider router={createMemoryAppRouter(["/"])} />);
  expect(await screen.findByRole("heading", { name: /video dubbing/i })).toBeVisible();
});
```

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/app/AppRouter.test.tsx`
Expected: FAIL because the router does not exist.

- [ ] **Step 3: Implement router and shell**

Root redirects to `/explore`. Use route-level `lazy()` for methods, compare, studio and evidence. AppShell contains OpenDub, Explore, Methods, Compare and Studio navigation with active state and a mobile menu.

- [ ] **Step 4: Move Studio without rewriting it**

Update relative imports and CSS paths. Add a route smoke assertion that `/studio` renders the existing project list heading.

- [ ] **Step 5: Verify**

Run: `pnpm --filter @opendub/web test -- --run && pnpm --filter @opendub/web build`
Expected: tests and TypeScript build pass.

- [ ] **Step 6: Commit**

```bash
git add apps/web
git commit -m "feat(web): route OpenDub around an atlas-first shell"
```

### Task 4: Typed Content Client

**Files:**

- Create: `apps/web/src/content/types.ts`
- Create: `apps/web/src/content/guards.ts`
- Create: `apps/web/src/content/client.ts`
- Create: `apps/web/src/content/assetUrl.ts`
- Create: `apps/web/src/content/client.test.ts`
- Create: `scripts/sync_atlas_content.py`
- Modify: `apps/web/package.json`

**Interfaces:**

- Produces: `getAtlasIndex()`、`getMethod(methodId)`、`getCase(caseId)`、`getReplay(caseId, methodId)`.
- Produces: `sync_atlas_content(source, publicRoot)` with hash-verified copy.

- [ ] **Step 1: Write fetch and invalid-content tests**

Mock fetch for a valid index, a 404 and a manifest with an unknown schema version. Assert `AtlasContentError` exposes `code`, `url` and actionable message.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/content/client.test.ts`
Expected: FAIL because content client modules do not exist.

- [ ] **Step 3: Implement generated-compatible types and runtime guards**

Mirror the v1 contracts exactly. Reject unknown major schema versions. Resolve only same-origin relative asset paths under `/atlas/`.

- [ ] **Step 4: Implement static content sync**

The script validates content first, copies only referenced public resources, calculates `content-lock.json` and removes stale files under `apps/web/public/atlas/`.

- [ ] **Step 5: Verify**

Run: `uv run python scripts/sync_atlas_content.py --check && pnpm --filter @opendub/web test -- --run src/content/client.test.ts`
Expected: no stale output and all tests pass.

- [ ] **Step 6: Commit**

```bash
git add apps/web/src/content scripts/sync_atlas_content.py apps/web/package.json
git commit -m "feat(content): load verified atlas manifests"
```

### Task 5: Timeline Controller and Playback Transport

**Files:**

- Create: `apps/web/src/features/timeline/TimelineController.ts`
- Create: `apps/web/src/features/timeline/time.ts`
- Create: `apps/web/src/features/timeline/TimelineContext.tsx`
- Create: `apps/web/src/features/timeline/useTimeline.ts`
- Create: `apps/web/src/features/timeline/PlaybackTransport.tsx`
- Create: `apps/web/src/features/timeline/GlobalTimeline.tsx`
- Test: `apps/web/src/features/timeline/TimelineController.test.ts`

**Interfaces:**

- Produces: `createTimelineController(initial: TimelineSnapshot): TimelineController`.
- Methods: `play(trackId)`、`pause()`、`seek(timeUs)`、`setDuration(durationUs)`、`subscribe(listener)`、`getSnapshot()`.

- [ ] **Step 1: Write deterministic time tests**

```ts
it("clamps seeks and keeps only one active track", () => {
  const timeline = createTimelineController({ caseId: "demo", durationUs: 2_000_000 });
  timeline.play("a");
  timeline.play("b");
  timeline.seek(3_000_000);
  expect(timeline.getSnapshot()).toMatchObject({
    activeTrackId: "b",
    currentTimeUs: 2_000_000,
  });
});
```

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/timeline/TimelineController.test.ts`
Expected: module not found.

- [ ] **Step 3: Implement external-store controller**

Use integer microseconds internally. Media adapters translate HTML media seconds only at the boundary. A new `play(trackId)` pauses the previous registered media track before starting.

- [ ] **Step 4: Implement keyboard-accessible transport**

Support Space play/pause, Left/Right seek by 100ms, Shift+Left/Right by 1s, Home/End. Ignore shortcuts when focus is in input, textarea or select.

- [ ] **Step 5: Verify**

Run: `pnpm --filter @opendub/web test -- --run src/features/timeline`
Expected: all timeline tests pass without fake timers leaking.

- [ ] **Step 6: Commit**

```bash
git add apps/web/src/features/timeline
git commit -m "feat(timeline): synchronize atlas media in microseconds"
```

### Task 6: Task Explorer Static Content and Core UI

**Files:**

- Create: `content/cases/authorized-demo/case.json`
- Create: `content/cases/authorized-demo/rights.md`
- Create: `content/cases/authorized-demo/inputs/`
- Create: `apps/web/src/features/explore/TaskExplorerPage.tsx`
- Create: `apps/web/src/features/explore/TaskEquation.tsx`
- Create: `apps/web/src/features/explore/InputLanes.tsx`
- Create: `apps/web/src/features/explore/VideoCueInspector.tsx`
- Create: `apps/web/src/features/explore/TaskOutput.tsx`
- Create: `apps/web/src/features/explore/task-explorer.css`
- Test: `apps/web/src/features/explore/TaskExplorerPage.test.tsx`

**Interfaces:**

- Consumes: `CaseManifest`, `TimelineController`.
- Produces: a fully interactive `/explore` route with input inspector and output tabs.

- [ ] **Step 1: Create an authorized synthetic case**

Use the repository FFmpeg example builder to create an 8 to 12 second redistributable clip, self-recorded or synthetic reference audio, text and generated placeholder output marked Concept. Record reviewer and rights evidence.

- [ ] **Step 2: Write accessibility and task-semantics tests**

Assert three input controls exist, Generated Speech and Dubbed Video are separate tabs, formal equation contains `A_hat` and method-specific control is disabled when unsupported.

- [ ] **Step 3: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/explore/TaskExplorerPage.test.tsx`
Expected: Task Explorer components missing.

- [ ] **Step 4: Implement the three-column task instrument**

Use stable grid tracks, real media aspect ratios, global timeline and Lucide icon controls. Video layer toggles show Scene, Face and Lip without changing layout dimensions.

- [ ] **Step 5: Implement natural and formal task views**

Natural view says `Video + Text + Reference Voice -> Dubbing Method -> Target Speech`. Formal view shows `A_hat = F_theta(V, X, A_ref, C)` and `Y = Mux(V, A_hat)` with accessible definitions.

- [ ] **Step 6: Verify**

Run: `uv run opendub atlas validate content && pnpm --filter @opendub/web test -- --run src/features/explore`
Expected: content and component tests pass.

- [ ] **Step 7: Commit**

```bash
git add content/cases apps/web/src/features/explore
git commit -m "feat(explore): explain the visual dubbing task interactively"
```

### Task 7: Guided Tour State Machine

**Files:**

- Create: `apps/web/src/features/explore/GuidedTourMachine.ts`
- Create: `apps/web/src/features/explore/GuidedTourOverlay.tsx`
- Test: `apps/web/src/features/explore/GuidedTourMachine.test.ts`
- Modify: `apps/web/src/features/explore/TaskExplorerPage.tsx`

**Interfaces:**

- Produces: states `scene`, `text`, `voice`, `visual_cues`, `method`, `output`, `complete`, `user_controlled`.

- [ ] **Step 1: Write transition tests**

Assert timed next steps, manual next/previous, any pointer/keyboard interaction transitions to `user_controlled`, and reduced-motion mode emits no path animation request.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/explore/GuidedTourMachine.test.ts`
Expected: state machine missing.

- [ ] **Step 3: Implement a pure reducer and timer coordinator**

Keep the transition reducer free of React. Durations are 5, 6, 6, 8, 8 and 7 seconds, totaling 40 seconds.

- [ ] **Step 4: Add accessible controls**

Provide pause, previous, next and replay. Announce stage changes in a polite live region without reading every animation update.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/explore`
Expected: all pass.

```bash
git add apps/web/src/features/explore
git commit -m "feat(explore): add an interruptible task tour"
```

### Task 8: Responsive, Accessibility and Visual QA

**Files:**

- Create: `apps/web/playwright.config.ts`
- Create: `apps/web/e2e/task-explorer.spec.ts`
- Create: `apps/web/e2e/helpers/assertNoOverflow.ts`
- Create: `apps/web/e2e/helpers/assertMediaReady.ts`
- Modify: `apps/web/package.json`
- Modify: `apps/web/src/styles/globals.css`
- Modify: `apps/web/src/styles/tokens.css`

**Interfaces:**

- Produces: repeatable screenshots and overflow/media assertions at five target viewports.

- [ ] **Step 1: Write failing Playwright checks**

Test route load, media nonblank, no horizontal document overflow, keyboard task traversal, reduced motion and screenshots at 1440x900, 1920x1080, 1280x720, 768x1024 and 390x844.

- [ ] **Step 2: Run and record initial failures**

Run: `pnpm --filter @opendub/web exec playwright test e2e/task-explorer.spec.ts`
Expected: failures identify missing responsive or media states.

- [ ] **Step 3: Fix layout with stable constraints**

Use `minmax(0, 1fr)`, fixed media aspect ratios and wrapped labels. At mobile widths transform the three columns into a controlled vertical sequence without hiding the timeline.

- [ ] **Step 4: Run full P1 verification**

```bash
uv run opendub atlas validate content
pnpm --filter @opendub/web test -- --run
pnpm --filter @opendub/web build
pnpm --filter @opendub/web exec playwright test e2e/task-explorer.spec.ts
```

Expected: all pass; screenshots contain populated video and signal areas.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "test(explore): verify responsive task experience"
```
