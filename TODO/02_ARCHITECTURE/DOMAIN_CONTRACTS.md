# Domain Contracts

## 版本约定

- 项目清单 Schema：`opendub.project/v1`
- 运行清单 Schema：`opendub.run/v1`
- 模型能力 Schema：`opendub.model-capabilities/v1`
- 指标报告 Schema：`opendub.metrics/v1`
- API 前缀：`/api/v1`

Schema 在 `schemas/` 中发布，变更遵循语义化版本。`v1` 内只允许新增可选字段，不允许改变已有字段含义。

## 标识符

- 所有领域对象使用 UUIDv7 字符串。
- 文件名不直接使用用户输入；用户输入仅作为展示名。
- 时间统一使用 UTC ISO 8601。
- 时间线位置以整数微秒保存，UI 可以显示帧或毫秒。
- 音频采样位置以整数 sample 保存。

## 核心数据类型

以下为未来 Python 接口的固定名称和职责。

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, Sequence

EmotionLabel = Literal[
    "neutral", "happy", "sad", "angry",
    "fearful", "surprised", "custom",
]

@dataclass(frozen=True)
class TimeRange:
    start_us: int
    end_us: int

    @property
    def duration_us(self) -> int: ...

@dataclass(frozen=True)
class EmotionSpec:
    label: EmotionLabel
    intensity: float
    valence: float | None = None
    arousal: float | None = None

@dataclass(frozen=True)
class VoiceReference:
    asset_id: str
    range: TimeRange | None
    consent_id: str
    speaker_label: str

@dataclass(frozen=True)
class DubbingSegment:
    id: str
    range: TimeRange
    text: str
    language: str
    character_id: str
    voice_reference_id: str
    emotion: EmotionSpec
    adapter_id: str
    accepted_candidate_id: str | None
    revision: int

@dataclass(frozen=True)
class DubbingRequest:
    project_id: str
    segment_id: str
    segment_revision: int
    video_path: Path
    text: str
    language: str
    target_range: TimeRange
    voice_path: Path
    emotion: EmotionSpec
    seed: int
    options: dict[str, object]

@dataclass(frozen=True)
class AudioArtifact:
    path: Path
    sample_rate: int
    channels: int
    duration_samples: int
    sha256: str

@dataclass(frozen=True)
class GenerationResult:
    audio: AudioArtifact
    adapter_id: str
    adapter_version: str
    model_id: str
    weights_sha256: str
    seed: int
    runtime_seconds: float
    metadata: dict[str, object]
```

## 模型适配器协议

```python
@dataclass(frozen=True)
class ModelCapabilities:
    schema_version: str
    adapter_id: str
    display_name: str
    version: str
    maturity: Literal["stable", "experimental", "planned"]
    languages: tuple[str, ...]
    requires_video: bool
    requires_face: bool
    requires_lip_roi: bool
    requires_reference_audio: bool
    emotion_labels: tuple[EmotionLabel, ...]
    supports_emotion_strength: bool
    supports_valence_arousal: bool
    supports_style_reference: bool
    supports_duration_control: bool
    output_type: Literal["waveform", "mel"]
    sample_rates: tuple[int, ...]
    minimum_vram_gb: float | None
    source_license: str
    weights_license: str
    runtime_isolation: Literal["in_process", "subprocess", "container"]

@dataclass(frozen=True)
class EnvironmentReport:
    ready: bool
    checks: tuple["EnvironmentCheck", ...]

@dataclass(frozen=True)
class PreparedInput:
    work_dir: Path
    manifest_path: Path
    cache_key: str

class ModelAdapter(Protocol):
    def capabilities(self) -> ModelCapabilities: ...
    def check_environment(self) -> EnvironmentReport: ...
    def prepare(self, request: DubbingRequest, work_dir: Path) -> PreparedInput: ...
    def generate(
        self,
        prepared: PreparedInput,
        *,
        progress: "ProgressSink",
        cancellation: "CancellationToken",
    ) -> GenerationResult: ...
    def cleanup(self) -> None: ...
```

`prepare()` 必须是确定性的。`generate()` 不得修改 `project.json`。`cleanup()` 必须可重复调用。

## 声码器协议

```python
@dataclass(frozen=True)
class MelArtifact:
    path: Path
    sample_rate: int
    hop_length: int
    n_mels: int
    sha256: str

class VocoderAdapter(Protocol):
    def capabilities(self) -> "VocoderCapabilities": ...
    def check_compatibility(self, mel: MelArtifact) -> None: ...
    def synthesize(
        self,
        mel: MelArtifact,
        *,
        progress: "ProgressSink",
        cancellation: "CancellationToken",
    ) -> AudioArtifact: ...
```

mel 的采样率、hop length、n_mels 不匹配时必须阻断，不能自动猜测。

## 指标协议

```python
MetricStatus = Literal["ok", "not_applicable", "unavailable", "failed"]

@dataclass(frozen=True)
class MetricResult:
    metric_id: str
    version: str
    status: MetricStatus
    value: float | None
    unit: str | None
    higher_is_better: bool | None
    details: dict[str, object]

class MetricPlugin(Protocol):
    def metric_id(self) -> str: ...
    def check_environment(self) -> EnvironmentReport: ...
    def evaluate(self, context: "EvaluationContext") -> MetricResult: ...
```

首版标准 Metric ID：

- `content.asr_error_rate`
- `speaker.cosine_similarity`
- `emotion.classification_match`
- `emotion.valence_arousal_distance`
- `sync.duration_error_ms`
- `audio.integrated_lufs`
- `audio.clipping_ratio`
- `audio.silence_ratio`

## 项目清单结构

```json
{
  "schema_version": "opendub.project/v1",
  "id": "019...",
  "name": "Authorized demo",
  "created_at": "2026-07-25T08:00:00Z",
  "updated_at": "2026-07-25T08:00:00Z",
  "revision": 1,
  "rights": {
    "declaration_version": "v1",
    "accepted_at": "2026-07-25T08:00:00Z",
    "material_source": "self_recorded"
  },
  "assets": [],
  "characters": [],
  "voice_references": [],
  "segments": [],
  "candidates": [],
  "exports": []
}
```

完整 JSON Schema 在实现阶段生成并作为 API 与前端类型生成源。

## 任务协议

任务类型：

- `media.analyze`
- `media.proxy`
- `segment.generate`
- `segment.evaluate`
- `project.generate`
- `project.evaluate`
- `project.render`
- `system.download_model`

任务状态：

`queued → preparing → running → finalizing → succeeded`，任一非终态可进入 `cancelling → cancelled` 或 `failed`；进程异常重启后为 `interrupted`。

事件结构：

```json
{
  "event_id": 42,
  "job_id": "019...",
  "time": "2026-07-25T08:00:00Z",
  "stage": "model.inference",
  "level": "info",
  "progress": 0.65,
  "message": "Generating acoustic features",
  "details": {}
}
```

`progress` 可以为 `null`。只有阶段内部确有可测总量时才发送数值。

## 错误协议

稳定错误码：

- `INPUT_INVALID`
- `RIGHTS_DECLARATION_REQUIRED`
- `ASSET_NOT_FOUND`
- `MEDIA_UNSUPPORTED`
- `MODEL_NOT_READY`
- `MODEL_CAPABILITY_MISMATCH`
- `MODEL_WEIGHTS_MISSING`
- `MODEL_LICENSE_NOT_ACCEPTED`
- `GPU_OUT_OF_MEMORY`
- `JOB_CANCELLED`
- `METRIC_UNAVAILABLE`
- `RENDER_FAILED`
- `PROJECT_CONFLICT`
- `INTERNAL_ERROR`

API 错误返回 `code`、`message`、`action`、`trace_id`。`details` 不得包含本地声音内容、完整台词或凭据。

## 并发与冲突

- 每次项目保存携带 `revision`。
- API 更新要求 `If-Match` 或请求体中的预期 revision。
- revision 不一致返回 `409 PROJECT_CONFLICT`。
- 运行任务绑定 `segment_revision`；片段被修改后旧结果仍保存，但不能自动成为当前候选。

## 工件目录

```text
projects/<project-id>/
├── project.json
├── assets/
├── proxies/
├── segments/<segment-id>/
│   ├── features/
│   └── candidates/<candidate-id>/
│       ├── audio.wav
│       ├── run.json
│       └── metrics.json
├── tracks/
├── exports/
├── reports/
└── logs/
```

共享权重位于独立模型缓存，不复制到项目目录。
