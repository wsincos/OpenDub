# Three-Method Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 HPMDubbing、StyleDubber、EmoDubber 建设为三套完整、可点击、可追溯的方法画布。

**Architecture:** 每套方法由 Method Manifest 定义节点、边、章节、信号槽和证据；React Flow 渲染图谱，ELK 生成稳定布局，Signal Renderer Registry 根据标准信号类型展示内容；方法专属交互只解释论文真实差异。

**Tech Stack:** React、TypeScript、React Flow、ELK、uPlot、Canvas、Vitest、Testing Library、Playwright、Python Atlas validator。

## Global Constraints

- 每个方法必须作为完整方法独立呈现。
- 方法之间只共享 UI renderer、时间控制和内容 Schema。
- 每个节点有问题、输入、输出、论文引用和信号槽。
- Concept 数值信号必须显示 `Illustrative`。
- 论文图只作引用；产品架构图重新绘制并注明来源。
- HPMDubbing_Vocoder 只作为 HPM 输出路径的支持组件。
- 方法状态从验证后的内容和 runtime 推导，不在 React 组件中写死。

---

### Task 1: Author and Validate Three Method Manifests

**Files:**

- Create: `content/methods/hpmdubbing/method.json`
- Create: `content/methods/hpmdubbing/copy.zh-CN.json`
- Create: `content/methods/hpmdubbing/copy.en.json`
- Create: `content/methods/styledubber/method.json`
- Create: `content/methods/styledubber/copy.zh-CN.json`
- Create: `content/methods/styledubber/copy.en.json`
- Create: `content/methods/emodubber/method.json`
- Create: `content/methods/emodubber/copy.zh-CN.json`
- Create: `content/methods/emodubber/copy.en.json`
- Create: `content/citations/papers.json`
- Create: `content/citations/bibliography.bib`
- Test: `tests/unit/atlas/test_core_method_content.py`

**Interfaces:**

- Produces: three valid `MethodManifest` documents with stable node IDs.
- Stable IDs include:
  - HPM: `lip_duration`, `face_affect`, `scene_emotion`, `hierarchical_prosody`, `mel_decoder`, `vocoder`.
  - Style: `phoneme_view`, `mpa`, `pla`, `usl`, `mel_decoder`, `refinement`.
  - Emo: `lpa`, `pe`, `speaker_identity`, `emotion_control`, `fuec`, `pngm`.

- [ ] **Step 1: Write required-content tests**

```python
@pytest.mark.parametrize(
    ("method_id", "required_nodes"),
    [
        ("galaxycong/hpmdubbing", {"lip_duration", "face_affect", "scene_emotion"}),
        ("galaxycong/styledubber", {"mpa", "pla", "usl"}),
        ("galaxycong/emodubber", {"lpa", "pe", "speaker_identity", "fuec", "pngm"}),
    ],
)
def test_core_methods_have_required_nodes(atlas, method_id, required_nodes):
    method = atlas.method(method_id)
    assert required_nodes <= {node.id for node in method.graph.nodes}
```

Also assert every node has at least one paper reference, all links use primary sources, and every overview path terminates at output.

- [ ] **Step 2: Run and confirm failure**

Run: `uv run pytest tests/unit/atlas/test_core_method_content.py -v`
Expected: manifests missing.

- [ ] **Step 3: Write HPMDubbing content**

Use the CVPR 2023 paper for task wording and Lip/Face/Scene relationships. Do not infer tensor shapes that are not confirmed in paper or source.

- [ ] **Step 4: Write StyleDubber content**

Use the ACL 2024 paper for MPA, PLA, USL and frame-to-phoneme motivation. Separate phoneme-level local style from utterance-level style.

- [ ] **Step 5: Write EmoDubber content**

Use the CVPR 2025 paper for LPA, PE, speaker identity adapting, FUEC and PNGM. Declare emotion category and intensity only here.

- [ ] **Step 6: Validate and manually review citations**

Run: `uv run opendub atlas validate content && uv run pytest tests/unit/atlas/test_core_method_content.py -v`
Expected: all manifests and citations pass.

- [ ] **Step 7: Commit**

```bash
git add content/methods content/citations tests/unit/atlas/test_core_method_content.py
git commit -m "content(methods): define the three complete dubbing methods"
```

### Task 2: Method Atlas Overview

**Files:**

- Create: `apps/web/src/features/methods/MethodAtlasPage.tsx`
- Create: `apps/web/src/features/methods/MethodEntry.tsx`
- Create: `apps/web/src/features/methods/ResearchProgression.tsx`
- Create: `apps/web/src/features/methods/method-atlas.css`
- Test: `apps/web/src/features/methods/MethodAtlasPage.test.tsx`
- Modify: `apps/web/src/app/AppRouter.tsx`

**Interfaces:**

- Consumes: `getAtlasIndex()` and method summaries.
- Produces: `/methods` and navigation to `/methods/:slug`.

- [ ] **Step 1: Write method-order and status tests**

Assert HPMDubbing, StyleDubber and EmoDubber appear once in 2023, 2024, 2025 order; each exposes Paper, Source and Explore; HPMDubbing_Vocoder is absent from the three main entries.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods/MethodAtlasPage.test.tsx`
Expected: page module missing.

- [ ] **Step 3: Implement the research progression layout**

Use a full-width chronological band, not independent marketing cards. Each method has a visible research question, contribution, conference, year and derived state.

- [ ] **Step 4: Add keyboard and mobile behavior**

Entries are links with visible focus. Mobile uses a vertical progression without horizontal scrolling.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods/MethodAtlasPage.test.tsx`

```bash
git add apps/web/src/features/methods apps/web/src/app/AppRouter.tsx
git commit -m "feat(methods): present the video dubbing research progression"
```

### Task 3: Deterministic Method Graph

**Files:**

- Create: `apps/web/src/features/methods/MethodCanvasPage.tsx`
- Create: `apps/web/src/features/methods/MethodGraph.tsx`
- Create: `apps/web/src/features/methods/MethodNode.tsx`
- Create: `apps/web/src/features/methods/method-layout.ts`
- Create: `apps/web/src/features/methods/method-store.ts`
- Create: `apps/web/src/features/methods/method-canvas.css`
- Test: `apps/web/src/features/methods/method-layout.test.ts`
- Test: `apps/web/src/features/methods/MethodGraph.test.tsx`
- Modify: `apps/web/package.json`

**Interfaces:**

- Produces: `layoutMethodGraph(graph: MethodGraph): Promise<PositionedGraph>`.
- Store fields: `selectedNodeId`, `pinnedSignalIds`, `chapterId`, `isOverviewPlaying`.

- [ ] **Step 1: Add React Flow and ELK**

Add pinned versions of `@xyflow/react` and `elkjs`. Import React Flow CSS once in the method feature entry.

- [ ] **Step 2: Write deterministic layout tests**

Run layout twice and assert identical node positions; assert all edges reference positioned nodes; assert input x positions are left of output x positions.

- [ ] **Step 3: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods/method-layout.test.ts`
Expected: layout module missing.

- [ ] **Step 4: Implement ELK layout**

Use `elk.direction=RIGHT`, fixed node width/height by kind and stable manifest order. Cache layout by `method.id + content hash`.

- [ ] **Step 5: Implement interactive graph**

Click selects a node; Enter/Space on focused node selects it; overview animates only along `overviewPath`; reduced motion updates selection without animated edges.

- [ ] **Step 6: Verify**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods`
Expected: layout and interaction tests pass.

- [ ] **Step 7: Commit**

```bash
git add apps/web/package.json pnpm-lock.yaml apps/web/src/features/methods
git commit -m "feat(methods): render deterministic interactive method graphs"
```

### Task 4: Component Inspector and Signal Dock

**Files:**

- Create: `apps/web/src/features/methods/MethodInspector.tsx`
- Create: `apps/web/src/features/methods/MethodChapterNav.tsx`
- Create: `apps/web/src/features/signals/SignalDock.tsx`
- Create: `apps/web/src/features/signals/SignalPanel.tsx`
- Create: `apps/web/src/features/signals/SignalRendererRegistry.ts`
- Create: `apps/web/src/features/signals/UnsupportedSignal.tsx`
- Test: `apps/web/src/features/methods/MethodInspector.test.tsx`
- Test: `apps/web/src/features/signals/SignalRendererRegistry.test.ts`

**Interfaces:**

- Produces: `registerSignalRenderer(type, renderer)` and `getSignalRenderer(type)`.
- Consumes: `MethodNode.visualizationSlots` and selected Replay/Concept artifacts.

- [ ] **Step 1: Write inspector completeness tests**

Select `lip_duration` and assert the inspector renders problem, consumes, produces, paper reference, mode label and Pin action. Missing signal renders an explicit unavailable explanation.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods/MethodInspector.test.tsx`
Expected: inspector missing.

- [ ] **Step 3: Implement the inspector**

Paper and code anchors open exact URLs. The inspector never renders raw HTML from content. Long lists wrap without resizing the graph.

- [ ] **Step 4: Implement a fixed-height signal dock**

Pinned panels have stable heights, reorder controls, unpin buttons and synchronized time. Empty state names which component and mode lacks data.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods src/features/signals`

```bash
git add apps/web/src/features/methods apps/web/src/features/signals
git commit -m "feat(methods): inspect components and pin observable signals"
```

### Task 5: Core Signal Renderers

**Files:**

- Create: `apps/web/src/features/signals/WaveformRenderer.tsx`
- Create: `apps/web/src/features/signals/PhonemeRenderer.tsx`
- Create: `apps/web/src/features/signals/ProsodyRenderer.tsx`
- Create: `apps/web/src/features/signals/SpectrogramRenderer.tsx`
- Create: `apps/web/src/features/signals/AlignmentRenderer.tsx`
- Create: `apps/web/src/features/signals/RoiRenderer.tsx`
- Create: `apps/web/src/features/signals/signal-renderers.css`
- Test: `apps/web/src/features/signals/renderers.test.tsx`
- Modify: `apps/web/package.json`

**Interfaces:**

- Each renderer consumes `{ descriptor, artifact, timeline }`.
- Produces accessible text summaries and Canvas/SVG visuals.

- [ ] **Step 1: Add uPlot and test fixtures**

Create short deterministic arrays with known time ranges, NaN unvoiced F0 and a 4x5 alignment matrix.

- [ ] **Step 2: Write renderer contract tests**

Assert time labels, units, illustrative labels, unvoiced gaps, matrix axis labels and current-time highlight.

- [ ] **Step 3: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/signals/renderers.test.tsx`
Expected: renderer modules missing.

- [ ] **Step 4: Implement waveform, phoneme and prosody**

Use Canvas for peaks, DOM for small token intervals and uPlot for F0/Energy. Do not connect missing F0 values.

- [ ] **Step 5: Implement spectrogram, alignment and ROI**

Use Canvas ImageData for matrices and real PTS for ROI frames. Use the same color range when renderer receives a comparison scale.

- [ ] **Step 6: Register all standard types and verify**

Run: `pnpm --filter @opendub/web test -- --run src/features/signals && pnpm --filter @opendub/web build`
Expected: all signal types in the three method manifests resolve to a renderer or explicit UnsupportedSignal.

- [ ] **Step 7: Commit**

```bash
git add apps/web/package.json pnpm-lock.yaml apps/web/src/features/signals
git commit -m "feat(signals): visualize time-aligned dubbing artifacts"
```

### Task 6: Method-Specific Concept Interactions

**Files:**

- Create: `apps/web/src/features/methods/concepts/HpmHierarchyView.tsx`
- Create: `apps/web/src/features/methods/concepts/StyleScaleView.tsx`
- Create: `apps/web/src/features/methods/concepts/EmoGuidanceView.tsx`
- Create: `content/methods/hpmdubbing/concept/`
- Create: `content/methods/styledubber/concept/`
- Create: `content/methods/emodubber/concept/`
- Test: `apps/web/src/features/methods/concepts/concepts.test.tsx`

**Interfaces:**

- HPM view consumes Scene/Face/Lip selections.
- Style view consumes `frame` or `phoneme` scale.
- Emo view consumes emotion label and intensity, returning explanation state only unless a matching Replay exists.

- [ ] **Step 1: Write truth-boundary tests**

Assert an Emo intensity change without a matching Replay changes the conceptual guidance display but does not change or relabel the audio source. Assert every synthetic curve shows `Illustrative`.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/methods/concepts`
Expected: concept modules missing.

- [ ] **Step 3: Implement HPM hierarchy**

Selecting Lip highlights duration; Face highlights F0/Energy; Scene highlights global emotion. Keep all three visible to preserve hierarchy.

- [ ] **Step 4: Implement Style scale switch**

Frame mode shows why multiple frames can map to one phoneme; Phoneme mode groups frames under stable phoneme intervals and reveals utterance style as a separate global band.

- [ ] **Step 5: Implement Emo guidance**

Render positive target direction, negative suppression directions and numeric intensity. Label it `Conceptual flow view` unless backed by Replay/Live.

- [ ] **Step 6: Verify and commit**

Run: `uv run opendub atlas validate content && pnpm --filter @opendub/web test -- --run src/features/methods`

```bash
git add apps/web/src/features/methods/concepts content/methods
git commit -m "feat(methods): add paper-specific concept interactions"
```

### Task 7: Evidence Room and Method Reproduction View

**Files:**

- Create: `apps/web/src/features/evidence/EvidenceRoomPage.tsx`
- Create: `apps/web/src/features/evidence/MethodEvidence.tsx`
- Create: `apps/web/src/features/evidence/StatusMatrix.tsx`
- Create: `apps/web/src/features/evidence/CitationActions.tsx`
- Test: `apps/web/src/features/evidence/EvidenceRoomPage.test.tsx`
- Modify: `apps/web/src/app/AppRouter.tsx`

**Interfaces:**

- Consumes: content manifests and `model-registry/upstreams.yaml` exported public status.
- Produces: one traceable view for Paper, Source, Commit, Code License, Weight Status, Content Modes and limitations.

- [ ] **Step 1: Write status honesty tests**

Assert no method displays Live when runtime is absent, unknown weight terms render `Unavailable`, and copy-citation exposes the exact BibTeX key.

- [ ] **Step 2: Run and confirm failure**

Run: `pnpm --filter @opendub/web test -- --run src/features/evidence`
Expected: Evidence components missing.

- [ ] **Step 3: Implement evidence aggregation**

Generate public status JSON from the validated registry at build time. Do not expose local paths or private URLs.

- [ ] **Step 4: Implement Evidence Room**

Use compact rows, not nested cards. Provide Paper, Source and Cite commands, limitations and date of last verification.

- [ ] **Step 5: Verify and commit**

Run: `pnpm --filter @opendub/web test -- --run src/features/evidence && pnpm --filter @opendub/web build`

```bash
git add apps/web/src/features/evidence apps/web/src/app/AppRouter.tsx scripts
git commit -m "feat(evidence): expose method provenance and availability"
```

### Task 8: Three-Method End-to-End and Visual QA

**Files:**

- Create: `apps/web/e2e/method-atlas.spec.ts`
- Create: `apps/web/e2e/method-canvas.spec.ts`
- Modify: `apps/web/playwright.config.ts`

**Interfaces:**

- Produces: desktop/mobile screenshots for Atlas and each Method Canvas.

- [ ] **Step 1: Write user-path tests**

Navigate from Task Explorer to each method, select two nodes, pin one signal, open paper evidence, refresh deep link and use browser back.

- [ ] **Step 2: Add canvas-pixel and overflow checks**

Verify graph canvas has non-background pixels, nodes are inside bounds, labels do not overlap edges at 1440x900 and 390x844, and reduced motion disables edge travel.

- [ ] **Step 3: Run and fix failures**

Run: `pnpm --filter @opendub/web exec playwright test e2e/method-atlas.spec.ts e2e/method-canvas.spec.ts`

- [ ] **Step 4: Run full M2 verification**

```bash
uv run opendub atlas validate content
uv run pytest tests/unit/atlas -q
pnpm --filter @opendub/web test -- --run
pnpm --filter @opendub/web build
pnpm --filter @opendub/web exec playwright test
```

- [ ] **Step 5: Commit**

```bash
git add apps/web/e2e
git commit -m "test(methods): verify all interactive method canvases"
```
