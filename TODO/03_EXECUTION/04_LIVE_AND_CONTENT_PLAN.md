# Live, Content and Grant Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成可公开的三方法内容、授权 Replay、条件式 Live 运行和与真实产品一致的申报演示证据包。

**Architecture:** 内容生产与 Live 运行分开推进。Concept 和合法历史 Demo 可以先发布；同输入比较只有在结果确实共享输入时开放；Live 必须通过源码、权重、许可、输入契约和真实推理五项准入，并通过 VisualizationProvider 输出标准信号。

**Tech Stack:** OpenDub Atlas SDK、FFmpeg、现有 Adapter Runtime、Pydantic、FastAPI、Playwright、OBS 或系统录屏、DaVinci Resolve/Premiere/FFmpeg。

## Global Constraints

- 没有 checkpoint 不阻止 Concept 和合法 Replay。
- 不同输入的历史 Demo 只能分别展示，不能进入同输入 Comparison Lab。
- 权重 URL 可访问不等于允许再分发。
- Live 失败时保持失败状态，不自动播放 Replay 并继续显示 Live。
- 申报影片录制的所有功能必须来自固定发布 commit。
- 每个公开媒体文件有 rights evidence 和 SHA-256。
- 三套方法内容由作者或项目负责人逐节点确认。

---

### Task 1: Audit Existing Demo and Paper Assets

**Files:**

- Create: `docs/audits/atlas-content-inventory.md`
- Create: `docs/audits/atlas-asset-rights.csv`
- Create: `content/source-inventory.json`
- Test: `tests/unit/atlas/test_source_inventory.py`
- Modify: `licenses/UPSTREAM_AUDIT.md`
- Modify: `licenses/MODEL_WEIGHTS.md`

**Interfaces:**

- Produces: one inventory row per paper figure, demo audio/video, checkpoint link, source file and preprocessing artifact.
- Status values: `usable_public`, `usable_local`, `permission_required`, `unknown`, `excluded`.

- [ ] **Step 1: Inventory exact upstream commits**

Inspect fixed commits already recorded for EmoDubber, HPMDubbing and StyleDubber. Record every demo page, media file, model link, code license and explicit asset statement.

- [ ] **Step 2: Write inventory validation tests**

Assert every asset has source URL, upstream commit, media type, copyright owner if known, public display decision, redistribution decision and reviewer.

- [ ] **Step 3: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_source_inventory.py -v`
Expected: inventory file missing.

- [ ] **Step 4: Classify assets conservatively**

Unknown is not usable. Paper publication permission does not automatically grant redistribution of film clips, datasets, voices or checkpoints.

- [ ] **Step 5: Verify and commit**

Run: `uv run pytest tests/unit/atlas/test_source_inventory.py -v`

```bash
git add docs/audits content/source-inventory.json licenses tests/unit/atlas/test_source_inventory.py
git commit -m "docs(content): audit method demos and asset rights"
```

### Task 2: Produce Concept Assets

**Files:**

- Create: `content/methods/hpmdubbing/concept/concept.json`
- Create: `content/methods/styledubber/concept/concept.json`
- Create: `content/methods/emodubber/concept/concept.json`
- Create: `scripts/build_concept_assets.py`
- Test: `tests/unit/atlas/test_concept_assets.py`

**Interfaces:**

- Produces: deterministic Scene/Face/Lip, phoneme, prosody, alignment and flow explanation assets.
- All generated numeric assets use `mode=concept` and `illustrative=true`.

- [ ] **Step 1: Write deterministic asset tests**

Run generation twice and compare hashes. Assert all numeric signals declare units, time base and illustrative status.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_concept_assets.py -v`
Expected: builder missing.

- [ ] **Step 3: Implement reusable authorized visual input**

Use self-created geometric face/lip proxy frames or a newly recorded consenting speaker. Avoid copying paper figures or dataset movie frames.

- [ ] **Step 4: Generate method-specific explanation signals**

HPM: three hierarchical cue tracks. Style: frame-to-phoneme grouping and local/global style bands. Emo: LPA/PE alignment explanation and positive/negative conceptual guidance.

- [ ] **Step 5: Validate, visually inspect and commit**

Run:

```bash
uv run python scripts/build_concept_assets.py --check
uv run opendub atlas validate content
uv run pytest tests/unit/atlas/test_concept_assets.py -v
```

```bash
git add content/methods scripts/build_concept_assets.py tests/unit/atlas/test_concept_assets.py
git commit -m "content(concept): build traceable method explanations"
```

### Task 3: Build Method-Specific Replay Bundles

**Files:**

- Create: `content/cases/<authorized-case-id>/case.json`
- Create: `content/replays/<authorized-case-id>/<method-slug>/replay.json`
- Create: `docs/atlas/replay-catalog.md`
- Test: `tests/integration/atlas/test_public_replays.py`

**Interfaces:**

- Produces: zero or more legal Replay Bundles per method.
- A case may contain one method result and still serve a Method Canvas; it cannot serve Comparison Lab.

- [ ] **Step 1: Select only assets classified usable_public**

For each method, match video, text, reference speech and output. If an upstream Demo does not provide all inputs, record the limitation and omit unsupported input playback.

- [ ] **Step 2: Write public bundle tests**

Assert asset hashes, rights evidence, method/case IDs, playable media and no absolute paths. Reject `permission_required`, `unknown` and `usable_local`.

- [ ] **Step 3: Pack bundles**

Run `opendub atlas pack` for each approved method-specific result. Do not normalize away original evidence; create separate 720p proxies and waveform peaks.

- [ ] **Step 4: Inspect in all three Method Canvas pages**

Confirm Replay status, media playback, signal timing and evidence. Missing signals use explicit unavailable states.

- [ ] **Step 5: Verify and commit**

Run: `uv run pytest tests/integration/atlas/test_public_replays.py -v && uv run opendub atlas validate content`

```bash
git add content/cases content/replays docs/atlas/replay-catalog.md tests/integration/atlas
git commit -m "content(replay): publish authorized method results"
```

### Task 4: Enforce the Same-Input Comparison Gate

**Files:**

- Create: `src/opendub/atlas/comparison.py`
- Test: `tests/unit/atlas/test_comparison_gate.py`
- Modify: `apps/web/src/content/replayClient.ts`
- Modify: `docs/atlas/replay-catalog.md`

**Interfaces:**

- Produces: `check_comparison_case(case, replays) -> ComparisonGateReport`.
- Gate requires at least two results with identical case ID and verified common-input asset hashes.

- [ ] **Step 1: Write mismatch tests**

```python
def test_comparison_rejects_different_reference_audio(case, replay_a, replay_b):
    replay_b.input_evidence.reference_sha256 = "0" * 64
    report = check_comparison_case(case, [replay_a, replay_b])
    assert "COMPARE_REFERENCE_MISMATCH" in report.error_codes
```

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_comparison_gate.py -v`
Expected: comparison module missing.

- [ ] **Step 3: Implement gate**

Compare video, text and reference hashes plus crop/time range. Method-specific control differences are recorded but do not change common inputs.

- [ ] **Step 4: Apply release decision**

If no case passes, keep Comparison Lab code available with test fixtures, remove it from the public main navigation and state “same-input public results are being prepared.” Do not place different Demo videos side by side.

- [ ] **Step 5: Verify and commit**

Run: `uv run pytest tests/unit/atlas/test_comparison_gate.py -v && uv run opendub atlas validate content`

```bash
git add src/opendub/atlas/comparison.py tests/unit/atlas/test_comparison_gate.py apps/web/src/content docs/atlas
git commit -m "feat(compare): gate public comparisons on identical inputs"
```

### Task 5: Admit One Live Method

**Files:**

- Create: `adapters/<selected-method>/adapter.yaml`
- Create: `adapters/<selected-method>/adapter.py`
- Create: `adapters/<selected-method>/MODEL_CARD.md`
- Create: `adapters/<selected-method>/LICENSES.md`
- Create: `adapters/<selected-method>/tests/test_real_smoke.py`
- Modify: `model-registry/upstreams.yaml`
- Modify: `docs/adapters/model-status.md`

**Interfaces:**

- Produces: one `CompleteDubbingAdapter` selected by the first artifact that passes all admission gates.

- [ ] **Step 1: Select by evidence, not preference**

Run the existing research-backend gate for EmoDubber, HPMDubbing and StyleDubber. Select the first method with fixed source commit, accessible weight, explicit use terms, SHA-256 and an input fixture that may be used for testing.

- [ ] **Step 2: Stop this task if no method passes**

Record all failed gate checks in `docs/adapters/model-status.md`. Keep runtime status `unavailable`. Continue with Concept, Replay and申报影片 using accurate labels.

- [ ] **Step 3: Write a real smoke test before adapter code**

The test invokes the isolated runtime on one authorized 1 to 3 second clip, asserts non-empty audio, finite samples, expected sample rate, duration bound and run manifest provenance. Mark it `real_model` and skip only when the verified local artifact is absent.

- [ ] **Step 4: Implement the complete adapter**

Translate OpenDub inputs to that method's published input contract. Preserve its native preprocessing and internal graph. Do not import components from the other two methods.

- [ ] **Step 5: Run real verification**

Run:

```bash
uv run pytest adapters/<selected-method>/tests/test_real_smoke.py -m real_model -v
uv run opendub doctor
```

Expected: real audio and a complete run manifest, or the method remains unavailable.

- [ ] **Step 6: Commit only verified status**

```bash
git add adapters model-registry/upstreams.yaml docs/adapters/model-status.md
git commit -m "feat(adapter): admit a verified complete dubbing method"
```

### Task 6: VisualizationProvider Contract and Method Provider

**Files:**

- Create: `src/opendub/models/visualization.py`
- Create: `tests/contract/models/test_visualization_provider.py`
- Create: `adapters/<selected-method>/visualization.py`
- Test: `adapters/<selected-method>/tests/test_visualization.py`

**Interfaces:**

- Produces: `SignalDescriptorModel`, `SignalCollectionModel`, `VisualizationProvider`.
- Produces standard signal files under `run/artifacts/signals/`.

- [ ] **Step 1: Write contract tests**

Reject missing units/time bases, paths outside run directory, unregistered signal IDs, NaN/Inf values and Replay/Live artifacts marked illustrative.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/contract/models/test_visualization_provider.py -v`
Expected: visualization protocol missing.

- [ ] **Step 3: Implement protocol and atomic writer**

Write signal collection to a temporary directory, validate every file and rename atomically after the generation result is complete.

- [ ] **Step 4: Implement only signals genuinely available from the selected method**

Map native filenames or registered hooks to standard signal IDs. Missing signal slots remain missing; do not synthesize values.

- [ ] **Step 5: Verify and commit**

Run:

```bash
uv run pytest tests/contract/models/test_visualization_provider.py -v
uv run pytest adapters/<selected-method>/tests/test_visualization.py -m real_model -v
```

```bash
git add src/opendub/models/visualization.py tests/contract/models adapters/<selected-method>
git commit -m "feat(signals): export verified live method artifacts"
```

### Task 7: Live Atlas API and Failure Semantics

**Files:**

- Create: `src/opendub/api/atlas.py`
- Test: `tests/integration/api/test_atlas_runtime.py`
- Modify: `src/opendub/api/app.py`
- Modify: `apps/web/src/content/liveClient.ts`
- Modify: `apps/web/src/features/evidence/StatusMatrix.tsx`
- Modify: `apps/web/src/features/methods/MethodCanvasPage.tsx`

**Interfaces:**

- Produces:
  - `GET /api/v1/atlas/methods/{method_id}/status`
  - `GET /api/v1/atlas/runs/{run_id}/signals`
  - `POST /api/v1/atlas/runs/{run_id}/replay-export`

- [ ] **Step 1: Write unavailable, running, failed and complete tests**

Assert absent checkpoint returns `ready=false` with gate reasons; failed run never exposes partial signal manifest; complete run returns hash-verified signals.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/integration/api/test_atlas_runtime.py -v`
Expected: routes missing.

- [ ] **Step 3: Implement API without changing static content behavior**

API reads validated runtime evidence. It does not change Method Manifest files or public status.

- [ ] **Step 4: Bind live state in the UI**

If API is unreachable, display Offline and retain Concept/Replay. If a Live run fails, keep the error and an explicit “Open Replay” separate action.

- [ ] **Step 5: Verify and commit**

Run:

```bash
uv run pytest tests/integration/api/test_atlas_runtime.py -v
pnpm --filter @opendub/web test -- --run
```

```bash
git add src/opendub/api tests/integration/api apps/web/src
git commit -m "feat(live): bind verified runtime signals to the atlas"
```

### Task 8: Live-to-Replay Export

**Files:**

- Create: `src/opendub/atlas/export_run.py`
- Test: `tests/integration/atlas/test_export_run.py`
- Modify: `src/opendub/atlas/cli.py`

**Interfaces:**

- Produces: `export_run_to_replay(run_id, rights, output_dir) -> ReplayBundleModel`.

- [ ] **Step 1: Write privacy and completion tests**

Reject incomplete runs, non-distributable voice consent, missing run manifest, absolute local paths and unknown weight hash for `mode=opendub_run`.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/integration/atlas/test_export_run.py -v`
Expected: exporter missing.

- [ ] **Step 3: Implement explicit export**

Copy only allowlisted media and signals, remove private local filenames from display metadata, calculate new hashes and require reviewer details.

- [ ] **Step 4: Round-trip verify**

Pack, validate, load in browser and compare output audio hash with the run artifact.

- [ ] **Step 5: Commit**

```bash
git add src/opendub/atlas tests/integration/atlas/test_export_run.py
git commit -m "feat(replay): export authorized live runs"
```

### Task 9: Author Review and Content Freeze

**Files:**

- Create: `docs/atlas/author-review-checklist.md`
- Create: `docs/atlas/reviews/hpmdubbing.md`
- Create: `docs/atlas/reviews/styledubber.md`
- Create: `docs/atlas/reviews/emodubber.md`
- Create: `content/content-lock.json`
- Test: `tests/unit/atlas/test_author_review.py`

**Interfaces:**

- Produces: signed-off node/edge/content review and final content lock.

- [ ] **Step 1: Generate review sheets**

For every method list question, inputs, each node, each edge, each signal, every claim and citation URL.

- [ ] **Step 2: Record reviewer decision per item**

Use `approved`, `corrected` or `excluded`, with reviewer name and date. Apply corrections to manifest before lock.

- [ ] **Step 3: Enforce review in release validation**

Tests fail if any core node or claim lacks an approved review entry.

- [ ] **Step 4: Build content lock**

Hash every manifest and public asset. The film recording commit records this lock hash.

- [ ] **Step 5: Verify and commit**

Run: `uv run opendub atlas validate content && uv run pytest tests/unit/atlas/test_author_review.py -v`

```bash
git add docs/atlas/reviews docs/atlas/author-review-checklist.md content/content-lock.json
git commit -m "content(atlas): freeze author-reviewed method content"
```

### Task 10: Grant Film and Release Evidence

**Files:**

- Create: `docs/grant/film/final-shot-log.csv`
- Create: `docs/grant/film/fact-check.md`
- Create: `docs/grant/film/release-evidence.md`
- Modify: `docs/grant/demo-script.md`
- Modify: `docs/grant/evidence-index.md`
- Modify: `README.md`

**Interfaces:**

- Produces: 2:40 master, 60-second cut, 30-second cut, poster frames and reproducibility log.

- [ ] **Step 1: Freeze the demo environment**

Record commit, content-lock hash, browser version, OS, resolution, font files, local URLs and whether each shot is Concept, Replay or Live.

- [ ] **Step 2: Run the recording preflight**

Execute full tests, open every shot route, cache all media, disable notifications and confirm no private paths or tokens appear.

- [ ] **Step 3: Record clean UI plates**

Capture 1920x1080 at 60fps following [DEMO_FILM/SHOTLIST.md](../04_OPEN_SOURCE/DEMO_FILM/SHOTLIST.md). Record cursor separately only if post-production needs emphasis.

- [ ] **Step 4: Edit and label**

Every Replay or Concept shot retains a visible mode label. Live progress is included only if Task 5 passed with the same release artifact.

- [ ] **Step 5: Fact-check frame by frame**

Map every narration claim to paper, source, test or run evidence. Remove any sentence without evidence.

- [ ] **Step 6: Export and verify**

Export H.264/AAC 1080p master, 60-second and 30-second cuts. Check audio peaks, subtitle safe area, dropped frames and final file hashes.

- [ ] **Step 7: Run release gate**

```bash
make check
uv run opendub atlas validate content
pnpm --filter @opendub/web exec playwright test
git diff --check
```

- [ ] **Step 8: Commit release evidence**

```bash
git add docs/grant README.md
git commit -m "docs(grant): publish the verified OpenDub demonstration"
```
