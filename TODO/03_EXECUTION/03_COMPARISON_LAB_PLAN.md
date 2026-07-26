# Comparison Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在相同视频、文本和参考语音下，对 HPMDubbing、StyleDubber、EmoDubber 的授权结果进行同步、可信、可追溯比较。

**Architecture:** Case Manifest 保存共同输入，Replay Bundle 保存单方法输出和信号；Python packer 负责媒体探测、hash、rights 和时间校验；React Comparison Lab 用单一 TimelineController 互斥播放候选，并将共同指标与方法特定能力分开。

**Tech Stack:** Pydantic、FFprobe、Typer、React、Zustand、Canvas、Web Audio、Vitest、Playwright。

## Global Constraints

- 同一比较只能引用一个 Case Manifest。
- 不允许为某方法偷偷更换视频、文本或参考语音。
- 播放切换保持相同时间位置且只能有一条结果发声。
- 音量标准化只影响试听增益，不覆盖或重编码原始结果。
- 指标预处理、版本和方向必须相同。
- 不适用显示 `N/A`，缺失显示 `Unavailable`。
- “最好”只能指当前案例、当前指标和当前证据。
- 无权公开的结果不能进入申报构建。

---

### Task 1: Replay Bundle Packer and Inspector

**Files:**

- Create: `src/opendub/atlas/pack.py`
- Create: `src/opendub/atlas/media_validation.py`
- Create: `src/opendub/atlas/inspect.py`
- Test: `tests/unit/atlas/test_pack.py`
- Test: `tests/integration/atlas/test_replay_media.py`
- Modify: `src/opendub/atlas/cli.py`

**Interfaces:**

- Produces: `pack_replay(spec: ReplayPackSpec, output: Path) -> ReplayBundleModel`.
- CLI: `opendub atlas pack PACK_SPEC --output DIR`.
- CLI: `opendub atlas inspect REPLAY_DIR`.

- [ ] **Step 1: Write hash, path and duration failure tests**

```python
def test_pack_rejects_output_longer_than_case_window(pack_spec):
    pack_spec.output_speech = wav_fixture(duration_s=3.0)
    pack_spec.case_duration_us = 2_000_000
    with pytest.raises(AtlasPackError, match="ATLAS_OUTPUT_DURATION"):
        pack_replay(pack_spec, pack_spec.output)
```

Also reject asset paths outside the staging root, missing rights evidence and a declared hash that differs from the file.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_pack.py -v`
Expected: packer module missing.

- [ ] **Step 3: Implement deterministic packing**

Probe media with existing FFprobe wrapper, calculate SHA-256, store relative POSIX paths, normalize manifest ordering and write bundle atomically.

- [ ] **Step 4: Implement inspection**

Print method, case, source mode, duration, assets, rights, metrics and every signal with mode. Exit `2` on invalid content.

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/unit/atlas/test_pack.py tests/integration/atlas/test_replay_media.py -v`
Expected: all pass using generated synthetic media.

- [ ] **Step 6: Commit**

```bash
git add src/opendub/atlas tests/unit/atlas/test_pack.py tests/integration/atlas
git commit -m "feat(replay): pack and inspect traceable method results"
```

### Task 2: Comparison Fixture and Replay Content Client

**Files:**

- Create: `tests/fixtures/atlas/comparison/`
- Create: `apps/web/src/content/replayClient.ts`
- Test: `apps/web/src/content/replayClient.test.ts`
- Modify: `apps/web/src/content/client.ts`

**Interfaces:**

- Produces: `getComparisonCase(caseId) -> Promise<ComparisonCase>`.
- `ComparisonCase.results` only contains validated and public-display-allowed bundles.

- [ ] **Step 1: Generate a test-only three-result case**

Generate three distinguishable sine/chirp WAV files and one synthetic video. Mark every result `testing_only=true`; keep the fixture outside public Atlas content.

- [ ] **Step 2: Write result-filter tests**

Assert invalid hash, non-public rights and wrong case ID results are excluded with visible diagnostics, not silently accepted.

- [ ] **Step 3: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/content/replayClient.test.ts`
Expected: replay client missing.

- [ ] **Step 4: Implement replay loading**

Load case first, then result manifests in declared order. Return `availableResults` and `rejectedResults` so Evidence can explain omissions.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/content/replayClient.test.ts`

```bash
git add tests/fixtures/atlas/comparison apps/web/src/content
git commit -m "feat(compare): load case-bound replay results"
```

### Task 3: Mutually Exclusive Candidate Playback

**Files:**

- Create: `apps/web/src/features/compare/compare-store.ts`
- Create: `apps/web/src/features/compare/MediaTrackRegistry.ts`
- Create: `apps/web/src/features/compare/CandidateTrack.tsx`
- Test: `apps/web/src/features/compare/MediaTrackRegistry.test.ts`
- Test: `apps/web/src/features/compare/CandidateTrack.test.tsx`

**Interfaces:**

- Produces: `registerTrack(trackId, mediaElement)` and `activateTrack(trackId, timeUs)`.
- Store: `activeResultId`, `currentTimeUs`, `blindMode`, `revealed`, `preference`.

- [ ] **Step 1: Write no-overlap and seek tests**

Register three fake media elements. Activate A at 800ms, then B. Assert A paused, B currentTime is 0.8 seconds and no third element plays.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare/MediaTrackRegistry.test.ts`
Expected: registry missing.

- [ ] **Step 3: Implement playback registry**

Handle rejected `play()` promises, ended events and seek precision. Conversion between seconds and microseconds happens only in this adapter.

- [ ] **Step 4: Implement stable candidate tracks**

Each track has fixed waveform height, play button, current time, duration, status and method/candidate label. Dynamic metrics must not shift controls.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare`

```bash
git add apps/web/src/features/compare
git commit -m "feat(compare): switch candidates without overlapping audio"
```

### Task 4: Comparison Lab Page

**Files:**

- Create: `apps/web/src/features/compare/ComparisonLabPage.tsx`
- Create: `apps/web/src/features/compare/CommonInputs.tsx`
- Create: `apps/web/src/features/compare/ComparisonToolbar.tsx`
- Create: `apps/web/src/features/compare/comparison-lab.css`
- Test: `apps/web/src/features/compare/ComparisonLabPage.test.tsx`
- Modify: `apps/web/src/app/AppRouter.tsx`

**Interfaces:**

- Consumes: `ComparisonCase`, timeline and media registry.
- Produces: `/compare/:caseId`.

- [ ] **Step 1: Write common-input and state tests**

Assert the page renders video/text/reference once, result tracks separately, rejects a one-result case as “comparison unavailable”, and preserves time when switching.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare/ComparisonLabPage.test.tsx`
Expected: page missing.

- [ ] **Step 3: Implement shared-input layout**

Use one video at top, input summary beside it and equal-height tracks below. Do not duplicate video inside result cards.

- [ ] **Step 4: Add A/B/C keyboard switching**

Keys `1`, `2`, `3` activate candidates outside form fields. Space toggles active candidate. Announce active candidate without reading method identity in blind mode.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare`

```bash
git add apps/web/src/features/compare apps/web/src/app/AppRouter.tsx
git commit -m "feat(compare): add a same-input dubbing comparison lab"
```

### Task 5: Blind Listening

**Files:**

- Create: `apps/web/src/features/compare/BlindListening.tsx`
- Create: `apps/web/src/features/compare/blind-order.ts`
- Test: `apps/web/src/features/compare/BlindListening.test.tsx`
- Test: `apps/web/src/features/compare/blind-order.test.ts`

**Interfaces:**

- Produces: `createBlindOrder(caseId, resultIds, sessionSeed)`.
- Produces: preference `{ caseId, anonymousChoice, resultId, createdAt }` stored locally only.

- [ ] **Step 1: Write deterministic anonymization tests**

Same case and seed yield same A/B/C order; different seed changes order; method names and source URLs do not occur in blind track accessible names before reveal.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare/blind-order.test.ts`
Expected: module missing.

- [ ] **Step 3: Implement blind ordering and reveal state**

Use a small deterministic seeded shuffle. Store preference after explicit submit, then allow reveal. Do not send telemetry.

- [ ] **Step 4: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare`

```bash
git add apps/web/src/features/compare
git commit -m "feat(compare): add local blind listening"
```

### Task 6: Comparable Metrics and Signal Scale

**Files:**

- Create: `apps/web/src/features/compare/MetricComparison.tsx`
- Create: `apps/web/src/features/compare/metric-policy.ts`
- Create: `apps/web/src/features/compare/ComparisonSignalView.tsx`
- Test: `apps/web/src/features/compare/metric-policy.test.ts`
- Test: `apps/web/src/features/compare/MetricComparison.test.tsx`

**Interfaces:**

- Produces: `buildComparableMetrics(results) -> MetricColumn[]`.
- Produces: a shared renderer scale for mel/F0/energy only when normalization metadata matches.

- [ ] **Step 1: Write metric intersection tests**

Given metrics with differing versions, return separate incompatible entries; given an Emo-only control metric, display N/A for HPM and Style; never coerce unavailable to zero.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare/metric-policy.test.ts`
Expected: policy missing.

- [ ] **Step 3: Implement metric policy**

Comparable key is `metric_id + version + preprocessing_hash`. Direction and unit must match. Provide explanation strings for N/A, unavailable and failed.

- [ ] **Step 4: Implement compact metric and signal views**

Use aligned columns and shared scale labels. Tooltips state that metrics support this case and are not a universal model ranking.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare`

```bash
git add apps/web/src/features/compare
git commit -m "feat(compare): enforce fair metric comparisons"
```

### Task 7: Comparison Report Export

**Files:**

- Create: `apps/web/src/features/compare/ComparisonSummary.tsx`
- Create: `apps/web/src/features/compare/export-report.ts`
- Test: `apps/web/src/features/compare/export-report.test.ts`

**Interfaces:**

- Produces: `buildComparisonReport(case, results, preference) -> ComparisonReport`.
- Exports UTF-8 Markdown and JSON from browser.

- [ ] **Step 1: Write provenance tests**

Assert report contains case hash, method IDs, result bundle hashes, metric versions, mode labels and preference scope. Assert it does not contain “best model”.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare/export-report.test.ts`
Expected: exporter missing.

- [ ] **Step 3: Implement report and download actions**

Markdown begins with `This report compares one authorized case and does not establish a universal model ranking.` JSON uses a versioned schema identifier.

- [ ] **Step 4: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/compare`

```bash
git add apps/web/src/features/compare
git commit -m "feat(compare): export traceable case-level reports"
```

### Task 8: Comparison End-to-End QA

**Files:**

- Create: `apps/web/e2e/comparison-lab.spec.ts`
- Modify: `apps/web/playwright.config.ts`

**Interfaces:**

- Produces: deterministic comparison screenshots and audio-state assertions.

- [ ] **Step 1: Write the full path**

Open case, play A, seek, switch B, enable blind mode, choose C, reveal, inspect metrics and download report.

- [ ] **Step 2: Assert media exclusivity in browser**

Evaluate all audio elements and assert at most one is not paused. Confirm currentTime differences are below 50ms after switching.

- [ ] **Step 3: Run visual QA**

Run at 1440x900, 1280x720 and 390x844. Check no track overflow, long method names wrap and metric states remain legible.

- [ ] **Step 4: Run full P4 verification**

```bash
uv run pytest tests/unit/atlas tests/integration/atlas -q
pnpm --filter @opendub/web test -- --run
pnpm --filter @opendub/web build
pnpm --filter @opendub/web exec playwright test e2e/comparison-lab.spec.ts
```

- [ ] **Step 5: Commit**

```bash
git add apps/web/e2e
git commit -m "test(compare): verify synchronized blind comparisons"
```
