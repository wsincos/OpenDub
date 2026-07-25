# OpenDub Method Atlas System Architecture

## 架构目标

OpenDub 将现有 `v0.0.1-alpha.0` 的本地 Studio 和 Python 媒体/运行基础保留为 Runtime Plane，在其上增加一个离线可用的 Method Atlas。

核心要求：

- Concept 和 Replay 不依赖 API、GPU 或 checkpoint。
- Live 通过现有 FastAPI 和隔离 Adapter Runtime 接入。
- 三套方法共享外围协议，不共享或拼接内部模块。
- 方法内容、图结构、信号和证据由版本化 manifest 驱动。
- 同一个 Replay Bundle 可以用于网站、申报录屏和离线文档。

## 四个平面

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Experience Plane                                                    │
│ Task Explorer | Method Atlas | Method Canvas | Compare | Evidence   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ typed content/runtime clients
┌──────────────────────────────▼──────────────────────────────────────┐
│ Content Plane                                                       │
│ Method manifests | Concept assets | Cases | Replay bundles          │
│ Schema validation | rights metadata | hashes | citations            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ optional live binding
┌──────────────────────────────▼──────────────────────────────────────┐
│ Runtime Plane                                                       │
│ Existing FastAPI | Project/Media | Jobs | Complete Method Adapters  │
│ VisualizationProvider | Run manifest | Export                       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ evidence
┌──────────────────────────────▼──────────────────────────────────────┐
│ Evidence Plane                                                      │
│ papers | source commits | weight hashes | licenses | rights | QA    │
└─────────────────────────────────────────────────────────────────────┘
```

## Experience Plane

### 应用路由

React 应用使用 `react-router-dom`：

- `/explore`
- `/methods`
- `/methods/:methodId`
- `/compare/:caseId`
- `/studio`
- `/evidence`

根路径重定向 `/explore`。未知方法或案例显示结构化 Not Found，不回退到空画布。

### 前端模块

| 模块 | 责任 |
|---|---|
| `app/router` | 路由、懒加载、错误边界 |
| `features/explore` | 任务导览、输入输出关系 |
| `features/methods` | Atlas 列表与 Method Canvas |
| `features/timeline` | 全局微秒时间游标和播放同步 |
| `features/signals` | 波形、频谱、音素、韵律、对齐渲染 |
| `features/compare` | 同输入 A/B/C、盲听、指标 |
| `features/evidence` | 论文、代码、许可和状态 |
| `features/studio` | 现有本地项目与 Live 运行 |
| `content` | manifest 加载、Schema 类型和资源解析 |

### 图谱引擎

使用 `@xyflow/react` 处理节点、边、缩放、键盘和视口，使用 `elkjs` 进行确定性布局：

- graph manifest 只定义语义边和分组。
- 发布构建预计算布局并写入 layout cache。
- 客户端可重新适配视图，但不随机布局。
- 节点组件保持无业务逻辑，只消费 `MethodNode`。

### 时间同步引擎

`TimelineController` 是独立于具体播放器的状态机：

```ts
type PlaybackState = "idle" | "playing" | "paused" | "seeking" | "ended";

interface TimelineSnapshot {
  caseId: string;
  currentTimeUs: number;
  durationUs: number;
  playbackState: PlaybackState;
  activeTrackId: string | null;
  rate: number;
}
```

- 视频是 Task Explorer 和 Compare 的主时钟。
- 只有音频的视图使用 `AudioContext.currentTime` 校准。
- `requestVideoFrameCallback` 可用时以实际视频帧刷新。
- UI 高频进度不写入 React 全局树，使用外部 store + selector。
- seek、播放、暂停和轨道切换通过单一 controller 执行。
- 切换候选时保留 `currentTimeUs`，并确保其他音频暂停。

### 信号渲染

- 波形：预计算多分辨率 peaks，Canvas 渲染。
- F0/Energy：`uPlot`。
- 音素/duration：DOM virtualized timeline。
- mel/alignment：Canvas 或 WebGL tile renderer。
- Face/Lip ROI：视频 overlay + image strip。
- 图谱：React Flow。

不得用大量 SVG/DOM 点绘制长时序数组。

## Content Plane

### 内容类型

```text
MethodManifest
  -> graph nodes and edges
  -> chapters
  -> citations
  -> supported signal slots

CaseManifest
  -> common video/text/reference inputs
  -> rights
  -> available method results

ReplayBundle
  -> run evidence
  -> output media
  -> time-aligned signals
  -> metrics
```

### 加载路径

1. 构建时读取 `content/index.json`。
2. 只加载首页需要的方法摘要和默认案例摘要。
3. 进入方法路由后动态导入该方法 manifest。
4. 选择 Replay 后加载 bundle manifest。
5. 大媒体由静态资源 URL 按需加载。

### Content SDK

Python 包提供：

- `opendub.atlas.validate`
- `opendub.atlas.pack`
- `opendub.atlas.hash`
- `opendub.atlas.export_run`

CLI：

```bash
opendub atlas validate content/
opendub atlas pack path/to/run --case authorized-demo --method emodubber
opendub atlas inspect content/replays/authorized-demo/emodubber
```

构建失败条件：

- Schema 不合法。
- 资源缺失或 hash 不匹配。
- Replay 缺少 rights。
- Live/Replay 信号被标为 illustrative。
- 论文链接、source commit 或方法 ID 缺失。

## Runtime Plane

### 现有能力复用

继续使用当前实现：

- ProjectStore、ArtifactStore。
- FFprobe/FFmpeg 和媒体渲染。
- 模型 Registry 和 verified weights。
- 隔离 JSON Lines Adapter Runtime。
- Job Scheduler 和运行 manifest。
- FastAPI、CLI 和 Web Studio。

### Complete Method Adapter

每套方法是独立 Adapter：

```python
class CompleteDubbingAdapter(Protocol):
    def capabilities(self) -> ModelCapabilities: ...
    def check_environment(self) -> EnvironmentReport: ...
    def prepare(self, request: DubbingRequest, work_dir: Path) -> PreparedInput: ...
    def generate(self, prepared: PreparedInput, *, progress, cancellation) -> GenerationResult: ...
    def cleanup(self) -> None: ...
```

Adapter 可以复用该方法自己的声码器或支持性仓库，但不能导入另一套核心方法的内部模块来补齐能力。

### VisualizationProvider

方法可选实现：

```python
class VisualizationProvider(Protocol):
    def describe_signals(self) -> tuple[SignalDescriptor, ...]: ...
    def collect(
        self,
        prepared: PreparedInput,
        result: GenerationResult,
        output_dir: Path,
    ) -> SignalCollection: ...
```

`collect()` 只能读取本次运行产物或明确注册的 hook 输出。它不得修改生成结果，不得用随机数据补齐缺失信号。

### Live 到 Replay

```text
Live Run
  -> completed run manifest
  -> rights check
  -> VisualizationProvider artifacts
  -> normalize timestamps and media
  -> compute hashes
  -> Replay Bundle
  -> manual review
  -> public content
```

公开导出是显式动作。默认 Live 运行保留在本机。

## Evidence Plane

每个方法必须绑定：

- 论文标题、会议、年份、URL、BibTeX。
- 上游仓库 URL 和固定 commit。
- source license。
- weight URL、license、SHA-256 或 unavailable 原因。
- 输入样例来源和分发权。
- 方法状态变更记录。
- Concept 作者复核记录。
- Replay/Live QA 记录。

Evidence Room 从同一 manifest 生成，不能维护第二套易失真的手写状态表。

## API 扩展

Atlas 不依赖 API，但 Live 和私有内容使用：

```text
GET  /api/v1/atlas/methods
GET  /api/v1/atlas/methods/{method_id}/status
GET  /api/v1/atlas/runs/{run_id}/signals
POST /api/v1/atlas/runs/{run_id}/replay-export
GET  /api/v1/atlas/jobs/{job_id}/events
```

公开 Concept 和 Replay 在静态部署中直接读取文件。API 返回的信号契约必须与静态 Replay Bundle 相同。

## 离线和失败策略

- Atlas 静态资源加载失败：显示具体缺失资源和重试。
- API 不可用：Concept/Replay 正常，Studio 显示本地服务不可用。
- checkpoint 缺失：Live 禁用，解释许可或 hash 缺失，不影响 Replay。
- 某信号缺失：组件保留，检查器显示缺失原因。
- 媒体解码失败：展示资源元数据和下载入口，不自动替换其他案例。
- WebGL 不可用：mel/alignment 回退 Canvas。

## 安全边界

- 默认不上传用户素材。
- 公开 Replay 只能包含通过分发审计的资源。
- 声音授权记录与结果 bundle 绑定。
- 论文原图只作为引用证据，不直接复制为产品主体。
- HTML/Markdown 内容经过消毒，manifest 不允许任意脚本。
- 资源路径必须位于内容根，禁止 `..` 和外部绝对路径。

## 部署

### 申报公开版本

- Vite 静态构建。
- Concept 和公开 Replay 内置或托管于同源对象存储。
- GitHub Pages 或静态主机可以运行核心 Atlas。
- 不在前端暴露第三方权重下载凭证。

### 本地完整版本

- FastAPI + React。
- 本地项目和模型缓存。
- GPU Adapter Runtime。
- 同一前端根据 `/api/v1/health` 激活 Studio Live 功能。

### 发布产物

- `opendub-atlas-static.tar.gz`
- `opendub-replay-authorized-demo.tar.gz`
- Python wheel。
- Docker/Compose 本地版本。
- SBOM、NOTICE 和 content audit report。
