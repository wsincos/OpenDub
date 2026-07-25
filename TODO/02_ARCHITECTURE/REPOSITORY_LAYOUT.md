# Target Repository Layout

## 原则

- 现有 Python 核心、API 和 Studio 保持在原有目录。
- Atlas 内容与 React 组件分离。
- 方法事实写入 manifest，不散落在 JSX。
- Replay 大文件与源代码分离，可用 Git LFS、Release 或对象存储。
- 三个完整方法分别拥有适配器和内容目录，不建立跨方法内部模块目录。

## 目标结构

```text
OpenDub/
├── apps/
│   └── web/
│       ├── public/
│       │   └── atlas/
│       │       ├── content-lock.json
│       │       ├── concept/
│       │       └── replays/
│       └── src/
│           ├── app/
│           │   ├── App.tsx
│           │   ├── AppRouter.tsx
│           │   ├── AppShell.tsx
│           │   └── routes.ts
│           ├── content/
│           │   ├── client.ts
│           │   ├── types.ts
│           │   ├── guards.ts
│           │   └── assetUrl.ts
│           ├── features/
│           │   ├── explore/
│           │   ├── methods/
│           │   ├── timeline/
│           │   ├── signals/
│           │   ├── compare/
│           │   ├── evidence/
│           │   └── studio/
│           ├── components/
│           │   ├── controls/
│           │   ├── media/
│           │   ├── status/
│           │   └── layout/
│           ├── styles/
│           └── test/
├── content/
│   ├── index.json
│   ├── methods/
│   │   ├── hpmdubbing/
│   │   │   ├── method.json
│   │   │   ├── copy.zh-CN.json
│   │   │   ├── copy.en.json
│   │   │   └── concept/
│   │   ├── styledubber/
│   │   └── emodubber/
│   ├── cases/
│   │   └── authorized-demo/
│   │       ├── case.json
│   │       ├── rights.md
│   │       └── inputs/
│   ├── replays/
│   │   └── authorized-demo/
│   │       ├── hpmdubbing/
│   │       ├── styledubber/
│   │       └── emodubber/
│   └── citations/
│       ├── papers.json
│       └── bibliography.bib
├── schemas/
│   ├── method-v1.json
│   ├── atlas-index-v1.json
│   ├── case-v1.json
│   ├── replay-v1.json
│   └── signals-v1.json
├── src/opendub/
│   ├── atlas/
│   │   ├── models.py
│   │   ├── validation.py
│   │   ├── hashing.py
│   │   ├── pack.py
│   │   ├── export_run.py
│   │   └── cli.py
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── media/
│   ├── models/
│   ├── pipeline/
│   └── storage/
├── adapters/
│   ├── hpmdubbing/
│   │   ├── adapter.yaml
│   │   ├── adapter.py
│   │   ├── visualization.py
│   │   ├── MODEL_CARD.md
│   │   └── tests/
│   ├── styledubber/
│   └── emodubber/
├── tests/
│   ├── fixtures/atlas/
│   ├── unit/atlas/
│   ├── integration/atlas/
│   └── e2e/atlas/
├── docs/
│   ├── atlas/
│   ├── methods/
│   ├── grant/
│   └── audits/
└── TODO/
```

## 前端文件责任

### `features/explore`

```text
TaskExplorerPage.tsx
TaskEquation.tsx
InputLanes.tsx
VideoCueInspector.tsx
TaskOutput.tsx
GuidedTourMachine.ts
task-explorer.css
```

`TaskExplorerPage` 只编排组件。导览状态机和时间控制不能写成页面内的一组互相影响的 `useState`。

### `features/methods`

```text
MethodAtlasPage.tsx
MethodCard.tsx
MethodCanvasPage.tsx
MethodGraph.tsx
MethodNode.tsx
MethodInspector.tsx
MethodChapterNav.tsx
method-layout.ts
```

方法内容全部来自 `MethodManifest`。只允许 renderer registry 根据 `NodeKind` 或 `SignalType` 选择组件。

### `features/timeline`

```text
TimelineController.ts
TimelineContext.tsx
useTimeline.ts
PlaybackTransport.tsx
GlobalTimeline.tsx
time.ts
```

时间转换集中在 `time.ts`。禁止在各页面重复 `seconds * 1000` 或浮点时间比较。

### `features/signals`

```text
SignalPanel.tsx
SignalRendererRegistry.ts
WaveformRenderer.tsx
SpectrogramRenderer.tsx
PhonemeRenderer.tsx
ProsodyRenderer.tsx
AlignmentRenderer.tsx
RoiRenderer.tsx
signal-renderers.css
```

每个 renderer 只处理一种数据契约和绘图，不加载方法内容。

### `features/compare`

```text
ComparisonLabPage.tsx
CandidateTrack.tsx
BlindListening.tsx
MetricComparison.tsx
ComparisonSummary.tsx
compare-store.ts
```

### `features/studio`

将当前 `StudioApp.tsx` 和 `StudioShell.tsx` 移入此目录，先只调整 import，不在 Atlas 首个任务中重写 Studio。

## 内容文件责任

- `method.json`：方法事实、图节点、边、章节和信号槽。
- `copy.*.json`：多语言解释文案。
- `concept/`：自制图标、示意信号和经过复核的结构素材。
- `case.json`：共同输入和权利。
- `replay.json`：一次方法结果及证据。
- `content-lock.json`：构建产物，不手工编辑。

## 命名规则

- Method ID 使用 `owner/name`。
- URL slug 使用小写仓库名。
- TypeScript 类型和 React 组件使用 `PascalCase`。
- TypeScript 函数和变量使用 `camelCase`。
- Python、JSON 字段和 CLI 参数使用 `snake_case`。
- Signal ID 使用点分层级，如 `prosody.f0.predicted`。
- 时间字段以 `_us` 结尾。
- hash 字段明确算法，如 `sha256`。

## 不进入 Git 的内容

- checkpoint 和未经允许分发的权重。
- 未经授权的视频、声音和字幕。
- 私有 Live 运行目录。
- 原始数据集。
- node_modules、缓存、构建产物和本地数据库。

允许通过 Release 或外部存储分发的 Replay Bundle 必须在 `content/index.json` 记录 URL、hash、大小和权利状态。
