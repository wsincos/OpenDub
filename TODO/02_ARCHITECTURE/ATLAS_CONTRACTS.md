# Atlas Data Contracts

## Schema 版本

- Method Manifest：`opendub.method/v1`
- Atlas Index：`opendub.atlas-index/v1`
- Case Manifest：`opendub.case/v1`
- Replay Bundle：`opendub.replay/v1`
- Signal Collection：`opendub.signals/v1`

`v1` 内只能增加可选字段。改变字段语义、时间单位或状态含义必须发布新 major schema。

## TypeScript 核心类型

```ts
export type MethodId =
  | "galaxycong/hpmdubbing"
  | "galaxycong/styledubber"
  | "galaxycong/emodubber";

export type ContentMode = "concept" | "replay" | "live" | "planned";
export type RuntimeStatus = "unavailable" | "experimental" | "stable";

export interface SourceReference {
  repository: string; // immutable upstream repository URL
  commit: string; // exactly 40 lowercase hexadecimal characters
  license: string; // source-code license verified at the pinned source
}

export interface MethodManifest {
  schemaVersion: "opendub.method/v1";
  id: MethodId;
  slug: "hpmdubbing" | "styledubber" | "emodubber";
  title: string;
  shortTitle: string;
  conference: string;
  year: number;
  question: LocalizedText;
  contribution: LocalizedText;
  paper: PaperReference;
  source: SourceReference;
  runtimeStatus: RuntimeStatus;
  contentModes: ContentMode[];
  requiredInputs: InputKind[];
  optionalControls: ControlDescriptor[];
  graph: MethodGraph;
  chapters: MethodChapter[];
  citations: CitationReference[];
}
```

## 方法图

```ts
export type NodeKind =
  | "input"
  | "visual"
  | "text"
  | "voice"
  | "alignment"
  | "prosody"
  | "style"
  | "emotion"
  | "acoustic"
  | "generation"
  | "output";

export interface MethodNode {
  id: string;
  label: LocalizedText;
  shortLabel: string;
  kind: NodeKind;
  summary: LocalizedText;
  solves: LocalizedText;
  consumes: string[];
  produces: string[];
  paperRefs: PaperAnchor[];
  codeRefs: CodeAnchor[];
  visualizationSlots: VisualizationSlot[];
  group?: string;
}

export interface MethodEdge {
  id: string;
  source: string;
  target: string;
  signalIds: string[];
  label?: LocalizedText;
}

export interface MethodGraph {
  nodes: MethodNode[];
  edges: MethodEdge[];
  groups: MethodGroup[];
  overviewPath: string[];
  layout: "left-to-right";
}
```

校验规则：

- node ID 在方法内唯一。
- edge 两端节点必须存在。
- `overviewPath` 中节点必须形成可解释的有向主路径。
- `signalIds` 必须在方法 signal catalog 中存在。
- `source.repository`、`source.commit` 和 `source.license` 必须同时存在；源码许可不能从 checkpoint 许可推断。
- 禁止自环。
- 输入节点没有来自方法内部的入边。
- 输出节点没有流向方法内部的出边。

## 信号描述

```ts
export type SignalType =
  | "video.scene"
  | "video.face_roi"
  | "video.lip_roi"
  | "text.transcript"
  | "text.phonemes"
  | "audio.reference"
  | "audio.generated"
  | "acoustic.mel"
  | "prosody.duration"
  | "prosody.f0"
  | "prosody.energy"
  | "emotion.valence_arousal"
  | "emotion.category"
  | "alignment.matrix"
  | "embedding.projection"
  | "flow.trajectory"
  | "metric.scalar";

export interface SignalDescriptor {
  id: string;
  type: SignalType;
  label: LocalizedText;
  unit?: string;
  timeBinding: "none" | "intervals" | "uniform" | "media_pts";
  renderer: string;
  explanation: LocalizedText;
}

export interface SignalArtifact {
  signalId: string;
  mode: Exclude<ContentMode, "planned">;
  illustrative: boolean;
  asset: AssetReference;
  timeBase?: TimeBase;
  shape?: number[];
  dtype?: string;
  normalization?: NormalizationDescriptor;
}
```

规则：

- `mode=replay|live` 时 `illustrative` 必须为 false。
- `mode=concept` 且数值为人为设计时 `illustrative` 必须为 true。
- 时序信号必须定义时间绑定。
- F0、energy、mel 和 embedding 必须声明单位或 normalization。

## 案例

```ts
export interface CaseManifest {
  schemaVersion: "opendub.case/v1";
  id: string;
  title: LocalizedText;
  durationUs: number;
  inputs: {
    video: AssetReference;
    text: TimedTranscript;
    referenceSpeech: AssetReference;
  };
  rights: RightsRecord;
  results: CaseResultReference[];
  featured: boolean;
}
```

同输入比较要求所有 `CaseResultReference` 引用同一个 CaseManifest。方法额外控制记录在结果内，不能修改共同输入。

## Replay Bundle

```ts
export interface ReplayBundle {
  schemaVersion: "opendub.replay/v1";
  id: string;
  caseId: string;
  methodId: MethodId;
  createdAt: string;
  provenance: ReplayProvenance;
  rights: RightsRecord;
  outputSpeech: AssetReference;
  dubbedVideo?: AssetReference;
  signals: SignalArtifact[];
  metrics: MetricResult[];
}

export interface ReplayProvenance {
  mode: "historical_demo" | "opendub_run" | "author_export";
  sourceCommit?: string;
  adapterVersion?: string;
  weightsSha256?: string;
  runManifestSha256?: string;
  parameters: Record<string, JsonValue>;
  limitations: string[];
}
```

Replay 可以缺少 checkpoint hash，但必须明确 `mode=historical_demo` 并解释来源。它不能被标记为可复现 Live。

## 资源引用

```ts
export interface AssetReference {
  path: string;
  mediaType: string;
  byteSize: number;
  sha256: string;
  durationUs?: number;
  width?: number;
  height?: number;
  sampleRate?: number;
  channels?: number;
}
```

规则：

- `path` 是相对 bundle 根目录的 POSIX 路径。
- 禁止 scheme、绝对路径、`..` 和符号链接逃逸。
- `byteSize` 与 hash 在打包和 CI 中验证。
- 浏览器加载资源后无需重复 hash；发布构建负责完整性。

## 权利记录

```ts
export interface RightsRecord {
  videoSource: "self_created" | "public_domain" | "licensed" | "authorized_other";
  voiceSource: "self_recorded" | "public_domain" | "licensed" | "authorized_other";
  textSource: "self_created" | "public_domain" | "licensed" | "authorized_other";
  publicDisplayAllowed: boolean;
  redistributionAllowed: boolean;
  evidencePath: string;
  reviewer: string;
  reviewedAt: string;
}
```

公开构建只接受 `publicDisplayAllowed=true`。将 bundle 纳入下载包还要求 `redistributionAllowed=true`。

## 内容状态推导

UI 状态不是编辑人员手写：

```ts
function deriveContentModes(
  method: MethodManifest,
  cases: CaseManifest[],
  runtime: RuntimeProbe | null,
): ContentMode[] {
  // concept from validated method content
  // replay from at least one valid bundle
  // live from ready runtime and admitted adapter
}
```

`Live` 只有在 `runtime.ready=true`、source commit 固定、weight hash 验证和真实 smoke 记录存在时返回。

## 版本与迁移

- manifest 中保存 schema version。
- CI 为每个版本保留至少一个 fixture。
- v1 到 v2 使用显式迁移脚本，不在 UI loader 中静默猜测。
- 内容构建输出 `content-lock.json`，记录所有 manifest 和资源 hash。
