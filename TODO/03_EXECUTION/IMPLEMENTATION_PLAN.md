# OpenDub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从空仓库构建一个本地优先、视频感知、情感可控、可评测、可导出成片的 OpenDub `v0.1.0`。

**Architecture:** Python 模块化单体承载领域、媒体、任务、模型运行时和评测；FastAPI 与 Typer 分别提供服务和 CLI；React Web Studio 提供专业时间线工作台；模型通过能力声明和隔离适配器接入。

**Tech Stack:** Python 3.11、uv、Pydantic v2、FastAPI、Typer、SQLAlchemy/SQLite、FFmpeg、PyTorch 模型适配器、React、TypeScript、Vite、TanStack Query、Zustand、Radix、WaveSurfer、pytest、Vitest、Playwright、Docker Compose。

## Global Constraints

- 新增平台代码使用 Apache-2.0；上游代码和权重保留独立许可与 NOTICE。
- 默认绑定 `127.0.0.1`，默认零遥测，素材默认不离开本机。
- 核心 Python 包不得依赖 PyTorch；PyTorch 只进入模型适配器或指标环境。
- `project.json` 是项目真相源，SQLite 只做可重建索引。
- 时间线内部单位为整数微秒，音频位置为整数 sample。
- 所有模型参数必须由 `ModelCapabilities` 声明；不支持的参数不得静默忽略。
- Stable 模型必须通过真实权重烟雾测试，模拟适配器仅用于自动化测试。
- 所有 FFmpeg 调用使用参数数组，不经 shell。
- 所有下载权重必须有 SHA-256；许可未知时不得自动下载。
- 官方示例只能使用自制或明确允许再分发的素材。
- 每个任务遵循：失败测试 → 最小实现 → 通过测试 → 文档/类型检查 → 独立提交。

---

## Phase 0：仓库与证据基线

### Task 1：创建主仓库与治理文件

**Files:**

- Create: `README.md`
- Create: `LICENSE`
- Create: `NOTICE`
- Create: `CITATION.cff`
- Create: `CONTRIBUTING.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `SECURITY.md`
- Create: `.gitignore`
- Create: `.editorconfig`
- Create: `.gitattributes`
- Create: `.github/CODEOWNERS`

**Produces:** 可公开的 Apache-2.0 空骨架，明确项目身份、引用和安全入口。

- [ ] 在 GitHub 组织或账号下创建 `GalaxyCong/OpenDub`，默认分支为 `main`，启用 Issue、Discussion 和分支保护。
- [ ] 将 `00_PRODUCT/PROJECT_CHARTER.md` 中的一句话定位写入 README 首屏；README 此时只声明规划中的 `v0.1.0`，不得写“已支持”。
- [ ] 写入完整 Apache-2.0 许可证，并在 NOTICE 列出 HPMDubbing、StyleDubber、EmoDubber 与 HPMDubbing_Vocoder 的名称、URL 和“计划适配”状态。
- [ ] 配置 `.gitignore` 排除 `.venv/`、`node_modules/`、模型权重、项目素材、缓存、日志、`.partial` 文件和本地数据库。
- [ ] 运行 `git diff --check`，预期无空白错误。
- [ ] 提交：`chore(repo): establish OpenDub project governance`。

### Task 2：完成上游资产与许可审计

**Files:**

- Create: `model-registry/upstreams.yaml`
- Create: `licenses/UPSTREAM_AUDIT.md`
- Create: `licenses/THIRD_PARTY_CODE.md`
- Create: `licenses/MODEL_WEIGHTS.md`
- Create: `scripts/verify_registry.py`
- Test: `tests/unit/model_registry/test_upstream_audit.py`

**Interfaces:**

- Produces: `upstreams.yaml`，每项包含 `id`、`repository`、`commit`、`source_license`、`weights`、`paper`、`maturity`。

- [ ] 锁定 EmoDubber、HPMDubbing、StyleDubber、HPMDubbing_Vocoder、HDCode 的实际 commit，而不是使用浮动 `main`。
- [ ] 对每个仓库核验源代码许可证、子依赖、权重地址、权重条款、数据限制和论文引用。
- [ ] 将 CoSyncDiT 与 LLM-Flow-Dubber 标记为 `planned`，原因分别记录为“未见可接入代码/权重”和“当前为演示网站”。
- [ ] 写失败测试：当 Registry 中 Stable/Experimental 模型缺少 commit、许可证或权重校验和时，验证脚本退出非零。

```python
def test_registry_rejects_releasable_model_without_commit(tmp_path):
    registry = write_registry(tmp_path, maturity="experimental", commit="")
    result = validate_upstream_registry(registry)
    assert "commit is required" in result.errors
```

- [ ] 实现结构化 Registry 校验，不用字符串搜索 YAML。
- [ ] 运行 `uv run pytest tests/unit/model_registry/test_upstream_audit.py -v`，预期全部通过。
- [ ] 运行 `uv run python scripts/verify_registry.py model-registry/upstreams.yaml`，预期输出每个模型的审核状态。
- [ ] 提交：`docs(models): record upstream licensing and reproducibility baseline`。

### Task 3：建立 Python、Web 与自动化基础

**Files:**

- Create: `pyproject.toml`
- Create: `uv.lock`
- Create: `src/opendub/__init__.py`
- Create: `src/opendub/config.py`
- Create: `apps/web/package.json`
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `apps/web/vite.config.ts`
- Create: `apps/web/tsconfig.json`
- Create: `Makefile`
- Create: `.pre-commit-config.yaml`
- Test: `tests/unit/test_import.py`

**Produces:** `uv sync` 和 `pnpm install` 可重复执行，核心包不安装 torch。

- [ ] 用 `uv init --package` 建立 Python 3.11 包，配置 Ruff、mypy、pytest 和 coverage。
- [ ] 添加 Pydantic、FastAPI、Typer、Rich、SQLAlchemy、HTTPX、PyYAML、SoundFile 和 NumPy；确认依赖树中没有 torch。
- [ ] 用 Vite 建立 React TypeScript 应用，添加 TanStack Query、Zustand、Radix、Lucide、WaveSurfer、Vitest、Testing Library 和 Playwright。
- [ ] 写导入测试：

```python
def test_core_package_does_not_import_torch():
    import opendub
    assert "torch" not in sys.modules
```

- [ ] 配置 `make check` 顺序运行 Python 格式、Python 类型、Python 测试、Web lint、Web 类型和 Web 测试。
- [ ] 运行 `uv sync --all-groups`、`pnpm install --frozen-lockfile`、`make check`。
- [ ] 提交：`chore(build): bootstrap Python and web workspaces`。

---

## Phase 1：领域、存储与媒体基础

### Task 4：实现稳定标识、时间与领域模型

**Files:**

- Create: `src/opendub/domain/ids.py`
- Create: `src/opendub/domain/time.py`
- Create: `src/opendub/domain/project.py`
- Create: `src/opendub/domain/assets.py`
- Create: `src/opendub/domain/segments.py`
- Create: `src/opendub/domain/candidates.py`
- Create: `src/opendub/domain/jobs.py`
- Create: `src/opendub/domain/metrics.py`
- Create: `src/opendub/domain/errors.py`
- Create: `src/opendub/domain/transitions.py`
- Test: `tests/unit/domain/`

**Interfaces:**

- Produces: `Project`, `MediaAsset`, `VoiceReference`, `ConsentRecord`, `DubbingSegment`, `EmotionSpec`, `Candidate`, `Job`, `MetricResult`, `TimeRange`。

- [ ] 先为 UUIDv7 格式、时间窗正长度、情感强度范围和片段状态转换写失败测试。
- [ ] 实现冻结的数据值对象和 Pydantic 聚合模型；所有用户可修改对象包含 revision。
- [ ] 实现 `transition_segment(current, target)`，禁止从 `unconfigured` 直接进入 `synthesizing`。
- [ ] 实现 `Project.accept_candidate(segment_id, candidate_id, expected_revision)`，旧 revision 返回 `PROJECT_CONFLICT`。
- [ ] 运行 `uv run pytest tests/unit/domain -v`，预期全部通过。
- [ ] 运行 `uv run mypy src/opendub/domain`，预期 0 errors。
- [ ] 提交：`feat(domain): define versioned dubbing project model`。

### Task 5：发布 JSON Schema 与跨端类型

**Files:**

- Create: `schemas/project-v1.json`
- Create: `schemas/run-v1.json`
- Create: `schemas/model-capabilities-v1.json`
- Create: `schemas/metrics-v1.json`
- Create: `scripts/export_schemas.py`
- Create: `scripts/generate_web_types.sh`
- Test: `tests/unit/schemas/test_schema_roundtrip.py`

**Produces:** Python 模型与 JSON Schema 一致，Web 类型自动生成。

- [ ] 写一个最小合法项目 fixture 和每类非法 fixture。
- [ ] 确认 Python 校验与 JSON Schema 对这些 fixture 得出相同结论。
- [ ] 使用 Pydantic 导出 Schema，使用 OpenAPI/JSON Schema 类型生成工具生成 `apps/web/src/api/generated/`。
- [ ] 将生成差异检查加入 `make check`，Schema 变化但未更新前端类型时 CI 失败。
- [ ] 提交：`feat(schema): publish versioned cross-client contracts`。

### Task 6：实现原子项目存储和可重建索引

**Files:**

- Create: `src/opendub/storage/atomic.py`
- Create: `src/opendub/storage/project_store.py`
- Create: `src/opendub/storage/artifact_store.py`
- Create: `src/opendub/storage/sqlite_index.py`
- Test: `tests/unit/storage/`
- Test: `tests/integration/storage/test_index_rebuild.py`

**Interfaces:**

- Produces: `ProjectStore.create()`、`load()`、`save(expected_revision)`、`delete()`、`rebuild_index()`。

- [ ] 写失败测试，模拟写入中断后原 `project.json` 仍可读取。
- [ ] 实现同目录临时文件、flush、fsync、`os.replace` 的原子保存。
- [ ] 实现素材内容寻址与 SHA-256；禁止路径逃出项目根目录。
- [ ] 实现 SQLite 项目/任务索引，并从项目目录完全重建。
- [ ] 测试删除项目不删除共享模型缓存。
- [ ] 运行 `uv run pytest tests/unit/storage tests/integration/storage -v`。
- [ ] 提交：`feat(storage): add atomic project store and rebuildable index`。

### Task 7：实现 FFprobe 与安全 FFmpeg 执行器

**Files:**

- Create: `src/opendub/media/probe.py`
- Create: `src/opendub/media/ffmpeg.py`
- Create: `src/opendub/media/audio.py`
- Create: `src/opendub/media/proxy.py`
- Test: `tests/unit/media/test_commands.py`
- Test: `tests/integration/media/test_ffmpeg_runner.py`

**Interfaces:**

- Produces: `probe_media(path) -> MediaProbe`、`FfmpegRunner.run(args)`、`normalize_reference_audio()`、`create_proxy()`。

- [ ] 写测试确保带空格、分号和 Unicode 的文件名仍作为单个参数传入，任何路径不经 shell。
- [ ] 解析 FFprobe JSON，不解析人类可读文本。
- [ ] 为视频生成 720p H.264 代理、封面帧和单独原音轨。
- [ ] 将参考声音标准化为单声道 WAV，并计算静音、削波和时长检查。
- [ ] 使用仓库内生成的合成媒体 fixture 运行集成测试，不依赖版权素材。
- [ ] 提交：`feat(media): add safe media probing and normalization`。

### Task 8：实现台词导入、时间线与最终渲染

**Files:**

- Create: `src/opendub/media/timeline.py`
- Create: `src/opendub/media/render.py`
- Create: `src/opendub/media/waveform.py`
- Create: `src/opendub/application/ingest_service.py`
- Test: `tests/unit/media/test_subtitles.py`
- Test: `tests/integration/media/test_render.py`

**Interfaces:**

- Produces: `import_srt()`、`import_vtt()`、`assemble_dubbing_track()`、`mux_video()`。

- [ ] 为字幕重叠、零长度、非法时间码和 UTF-8 中文台词写测试。
- [ ] 导入时保留原字幕文本并生成标准微秒时间窗。
- [ ] 拼接片段时对空白区域填充静音，对冲突片段阻断并报告片段 ID。
- [ ] 支持原声保留、降低和移除三种混音模式。
- [ ] 验证最终 WAV 与视频时长误差不超过一个音频 sample frame。
- [ ] 提交：`feat(media): build timeline import and deterministic rendering`。

---

## Phase 2：模型插件、任务与真实生成

### Task 9：实现模型能力、注册表与权重管理

**Files:**

- Create: `src/opendub/models/capabilities.py`
- Create: `src/opendub/models/protocols.py`
- Create: `src/opendub/models/registry.py`
- Create: `src/opendub/models/manifests.py`
- Create: `src/opendub/models/weights.py`
- Test: `tests/unit/models/`

**Interfaces:**

- Produces: `ModelAdapter`、`VocoderAdapter`、`ModelRegistry.discover()`、`WeightManager.ensure()`。

- [ ] 按 `DOMAIN_CONTRACTS.md` 实现能力模型和协议。
- [ ] 写契约测试，验证适配器不能声明 `supports_emotion_strength=True` 却没有情感标签或连续情感输入。
- [ ] 实现显式下载许可确认、断点下载、大小检查、SHA-256 和原子落盘。
- [ ] 下载失败保留 `.partial`，但注册表不把它视为可用权重。
- [ ] 运行 Registry 测试和模拟 HTTP 下载测试。
- [ ] 提交：`feat(models): add capability registry and verified weight manager`。

### Task 10：实现隔离模型运行时

**Files:**

- Create: `src/opendub/models/runtime.py`
- Create: `src/opendub/models/subprocess_worker.py`
- Create: `src/opendub/pipeline/cancellation.py`
- Create: `src/opendub/observability/redaction.py`
- Test: `tests/contract/models/test_adapter_contract.py`
- Test: `tests/integration/models/test_subprocess_runtime.py`

**Interfaces:**

- Produces: `AdapterRuntime.prepare()`、`generate()`、`cancel()`、`release()`；JSON Lines 子进程协议。

- [ ] 定义握手、环境报告、进度、结果、错误和取消的 JSON Lines 消息。
- [ ] 用 DeterministicTestAdapter 写失败、成功、超时、取消和子进程崩溃测试。
- [ ] 实现 stdout 协议与 stderr 日志分离，避免模型打印污染协议。
- [ ] 实现进程组终止和清理，不遗留 GPU worker。
- [ ] 对日志中的本地绝对路径和声音文件名做脱敏。
- [ ] 提交：`feat(runtime): isolate model adapters behind a structured protocol`。

### Task 11：实现本地任务调度和可恢复流水线

**Files:**

- Create: `src/opendub/jobs/models.py`
- Create: `src/opendub/jobs/repository.py`
- Create: `src/opendub/jobs/events.py`
- Create: `src/opendub/jobs/scheduler.py`
- Create: `src/opendub/pipeline/stages.py`
- Create: `src/opendub/pipeline/cache.py`
- Create: `src/opendub/pipeline/planner.py`
- Create: `src/opendub/pipeline/executor.py`
- Test: `tests/unit/jobs/`
- Test: `tests/integration/pipeline/`

**Interfaces:**

- Produces: `JobScheduler.enqueue()`、`cancel()`、`events(after_id)`；`PipelinePlanner.plan_generation()`。

- [ ] 先写单 GPU 串行、CPU 有限并发、取消、进程重启转 interrupted 的测试。
- [ ] 实现任务事件持久化和单调 event ID。
- [ ] 实现阶段缓存键，输入、revision、权重或种子变化时缓存失效。
- [ ] 实现“从失败阶段重试”，已验证中间产物可以复用。
- [ ] 使用 DeterministicTestAdapter 完成端到端管线测试。
- [ ] 提交：`feat(pipeline): add recoverable local generation scheduler`。

### Task 12：审计并接入 EmoDubber

**Files:**

- Create: `adapters/emodubber/pyproject.toml`
- Create: `adapters/emodubber/adapter.yaml`
- Create: `adapters/emodubber/MODEL_CARD.md`
- Create: `adapters/emodubber/LICENSES.md`
- Create: `adapters/emodubber/src/opendub_adapter_emodubber/`
- Create: `adapters/emodubber/tests/`
- Create: `scripts/smoke_emodubber.sh`

**Interfaces:**

- Produces: `EmoDubberAdapter`，输出标准 WAV 或标准 mel。

- [ ] 在固定上游 commit 上跑通原始推理，记录真实环境、输入要求、权重、运行命令、显存和输出。
- [ ] 验证公开代码是否真正实现情感标签与强度控制；若未实现，适配器必须声明相应能力为 false，且 `v0.1.0` 发布被“情感核心能力门槛”阻断，直到团队提供可发布实现。
- [ ] 将硬编码路径改为由 `PreparedInput.manifest_path` 传入。
- [ ] 不允许要求用户替换 Lightning 的 site-packages；通过兼容封装或局部补丁解决。
- [ ] 写能力、输入转换、错误映射和确定性元数据测试。
- [ ] 使用真实权重和授权样本运行 `test_real_smoke.py`，测试通过后才将成熟度改为 Stable。
- [ ] 比较情感控制前后至少一个可计算情感指标，确认控制参数不是空操作。
- [ ] 提交：`feat(adapter-emodubber): add verified emotion-directed dubbing`。

### Task 13：接入 HPM HiFi-GAN 声码器

**Files:**

- Create: `adapters/hpm_vocoder/pyproject.toml`
- Create: `adapters/hpm_vocoder/adapter.yaml`
- Create: `adapters/hpm_vocoder/MODEL_CARD.md`
- Create: `adapters/hpm_vocoder/LICENSES.md`
- Create: `adapters/hpm_vocoder/src/opendub_adapter_hpm_vocoder/`
- Create: `adapters/hpm_vocoder/tests/`

**Interfaces:**

- Produces: `HpmVocoderAdapter`，支持经过验证的 16kHz 和 22050Hz 配置。

- [ ] 固定 HPMDubbing_Vocoder commit 和两个权重清单。
- [ ] 从权重或显式模型卡读取 sample rate、hop length、n_mels，不从文件名猜测。
- [ ] 为 mel 参数不兼容写失败测试。
- [ ] 使用合成 mel 与真实模型输出 mel 分别做烟雾测试。
- [ ] 检查输出无 NaN、不过度削波、采样率正确、时长与 mel 帧数一致。
- [ ] 提交：`feat(adapter-vocoder): add validated HPM HiFi-GAN rendering`。

### Task 14：实现生成应用服务

**Files:**

- Create: `src/opendub/application/generation_service.py`
- Create: `src/opendub/application/project_service.py`
- Create: `tests/integration/application/test_generate_segment.py`

**Interfaces:**

- Produces: `GenerationService.generate_segment()`、`generate_project()`、`accept_candidate()`。

- [ ] 验证参考声音授权、片段状态、模型能力和权重就绪。
- [ ] 通过 Planner 创建视频预处理、模型生成、声码器、后处理与评测阶段。
- [ ] 保存 `run.json`，包含所有追溯字段。
- [ ] 片段在生成期间被修改时，将结果保存为历史候选但不挂到当前 revision。
- [ ] 运行 DeterministicTestAdapter 集成测试和 EmoDubber 真实烟雾测试。
- [ ] 提交：`feat(application): orchestrate traceable segment generation`。

---

## Phase 3：Quality Lab、API 与 CLI

### Task 15：实现基础音频与同步指标

**Files:**

- Create: `src/opendub/evaluation/protocols.py`
- Create: `src/opendub/evaluation/registry.py`
- Create: `src/opendub/evaluation/sync.py`
- Create: `src/opendub/evaluation/audio_quality.py`
- Test: `tests/unit/evaluation/test_sync.py`
- Test: `tests/unit/evaluation/test_audio_quality.py`

**Produces:** duration error、LUFS、clipping ratio、silence ratio。

- [ ] 用已知长度与已知削波比例的合成 WAV 写失败测试。
- [ ] 实现 MetricStatus 四态，不可用指标不得返回 0。
- [ ] 统一指标精度、单位和 higher-is-better 元数据。
- [ ] 提交：`feat(metrics): add deterministic sync and audio checks`。

### Task 16：实现内容、音色和情感指标

**Files:**

- Create: `src/opendub/evaluation/content.py`
- Create: `src/opendub/evaluation/speaker.py`
- Create: `src/opendub/evaluation/emotion.py`
- Create: `src/opendub/evaluation/report.py`
- Create: `src/opendub/application/evaluation_service.py`
- Test: `tests/contract/evaluation/`
- Test: `tests/integration/evaluation/test_report.py`

**Produces:** 标准 JSON/CSV/HTML 或 Markdown 报告。

- [ ] 固定 ASR、speaker encoder 和 emotion classifier 的模型版本与权重。
- [ ] 分别构造匹配与明显不匹配样本，验证指标方向。
- [ ] 指标模型不支持输入语言时返回 `not_applicable`。
- [ ] 报告同时展示值、版本、输入摘要、状态和限制。
- [ ] 项目级汇总按片段时长加权，并保留原始片段值。
- [ ] 提交：`feat(metrics): add content voice and emotion evaluation`。

### Task 17：实现 FastAPI

**Files:**

- Create: `src/opendub/api/app.py`
- Create: `src/opendub/api/dependencies.py`
- Create: `src/opendub/api/errors.py`
- Create: `src/opendub/api/schemas.py`
- Create: `src/opendub/api/routes/projects.py`
- Create: `src/opendub/api/routes/assets.py`
- Create: `src/opendub/api/routes/segments.py`
- Create: `src/opendub/api/routes/models.py`
- Create: `src/opendub/api/routes/jobs.py`
- Create: `src/opendub/api/routes/reports.py`
- Create: `src/opendub/api/routes/exports.py`
- Test: `tests/integration/api/`

**Produces:** `/api/v1` REST 与 `/api/v1/jobs/{id}/events` SSE。

- [ ] 写项目 CRUD、revision 冲突、上传限制、能力查询、任务创建、取消、SSE 重连和导出测试。
- [ ] 将领域错误映射为稳定错误码与 HTTP 状态。
- [ ] 配置 localhost 默认绑定、受限 CORS 和上传大小。
- [ ] 生成 OpenAPI 并检查与 Web 类型无差异。
- [ ] 提交：`feat(api): expose local project and generation API`。

### Task 18：实现 CLI 与系统诊断

**Files:**

- Create: `src/opendub/cli/app.py`
- Create: `src/opendub/cli/output.py`
- Create: `src/opendub/cli/commands/doctor.py`
- Create: `src/opendub/cli/commands/init.py`
- Create: `src/opendub/cli/commands/analyze.py`
- Create: `src/opendub/cli/commands/generate.py`
- Create: `src/opendub/cli/commands/evaluate.py`
- Create: `src/opendub/cli/commands/render.py`
- Create: `src/opendub/application/doctor_service.py`
- Test: `tests/integration/cli/`

**Produces:** README 中承诺的七个命令及 JSON 输出模式。

- [ ] 为每个命令写 help 快照和成功/失败退出码测试。
- [ ] `doctor` 检查 FFmpeg、可写目录、GPU、模型 Registry、权重与适配器环境。
- [ ] 所有命令支持 `--json`，机器输出不混入 Rich 样式。
- [ ] `doctor --report` 的诊断包通过隐私扫描测试。
- [ ] 提交：`feat(cli): add reproducible command-line workflow and diagnostics`。

---

## Phase 4：专业 Web Studio

### Task 19：建立设计系统与应用框架

**Files:**

- Create: `apps/web/src/styles/tokens.css`
- Create: `apps/web/src/styles/globals.css`
- Create: `apps/web/src/app/router.tsx`
- Create: `apps/web/src/app/providers.tsx`
- Create: `apps/web/src/app/shell/StudioShell.tsx`
- Create: `apps/web/src/components/ui/`
- Test: `apps/web/src/app/shell/StudioShell.test.tsx`

**Produces:** 项目主页与四区 Studio 框架，符合 PRODUCT_EXPERIENCE。

- [ ] 定义 Ink/Canvas/Surface/Teal/Coral/Amber 等 CSS token、字体、间距、圆角和焦点。
- [ ] 实现顶部工具栏、左资源栏、中央工作区、右检查器和底部任务抽屉。
- [ ] 使用 Lucide 图标和 tooltip；不绘制自定义通用 SVG 图标。
- [ ] 写键盘导航、焦点和窄桌面布局测试。
- [ ] 在 1440×900、1280×720、390×844 截图检查无重叠；移动端展示只读结果模式。
- [ ] 提交：`feat(web): establish the OpenDub studio design system`。

### Task 20：实现项目、素材与授权流程

**Files:**

- Create: `apps/web/src/features/projects/`
- Create: `apps/web/src/features/assets/`
- Create: `apps/web/src/features/voices/`
- Create: `apps/web/src/api/client.ts`
- Create: `apps/web/src/api/events.ts`
- Test: `apps/web/src/features/projects/*.test.tsx`
- Test: `apps/web/e2e/project-ingest.spec.ts`

**Produces:** 新建项目、导入视频/台词/声音、授权确认和素材状态。

- [ ] 项目主页显示真实项目数据和进度，不使用营销 Hero。
- [ ] 上传显示探测、代理和失败恢复阶段。
- [ ] 参考声音在授权确认前不能绑定片段。
- [ ] 错误显示 code、action 和复制诊断信息，不显示原始 traceback。
- [ ] Playwright 完成创建项目与导入合成示例。
- [ ] 提交：`feat(web): add project ingestion and voice consent workflow`。

### Task 21：实现播放器、波形和时间线

**Files:**

- Create: `apps/web/src/features/player/`
- Create: `apps/web/src/features/timeline/`
- Create: `apps/web/src/features/segments/`
- Create: `apps/web/src/store/editorStore.ts`
- Test: `apps/web/src/features/timeline/*.test.tsx`
- Test: `apps/web/e2e/timeline-edit.spec.ts`

**Produces:** 播放头、缩放、片段选择、字幕编辑、波形和 revision 更新。

- [ ] 定义稳定时间轴尺寸和像素/微秒变换，hover 和选择不改变布局。
- [ ] 播放器与时间线双向同步，seek 误差小于一帧。
- [ ] 片段重叠、过短、过长和未配置状态有独立视觉反馈。
- [ ] 支持撤销/重做，操作只修改编辑会话，保存时提交 revision。
- [ ] Playwright 验证选择片段、编辑台词、保存和冲突提示。
- [ ] 提交：`feat(web): build synchronized video and dubbing timeline`。

### Task 22：实现情感、模型与候选检查器

**Files:**

- Create: `apps/web/src/features/emotion/`
- Create: `apps/web/src/features/models/`
- Create: `apps/web/src/features/candidates/`
- Create: `apps/web/src/features/jobs/`
- Test: `apps/web/src/features/emotion/*.test.tsx`
- Test: `apps/web/e2e/generate-review.spec.ts`

**Produces:** 能力驱动参数、任务进度、候选 A/B、指标摘要与确认。

- [ ] 从 API 能力声明生成控制项；不支持的情感标签和高级参数禁用并说明原因。
- [ ] 情感强度同时使用滑杆和数值输入，范围严格为 0–1。
- [ ] SSE 断线后使用 event ID 重连并补齐事件。
- [ ] 候选最多显示 5 个，具备波形、时长偏差、指标和运行信息。
- [ ] 确认候选前后 UI 与项目 revision 保持一致。
- [ ] 提交：`feat(web): add capability-aware generation and candidate review`。

### Task 23：实现评测、任务与导出

**Files:**

- Create: `apps/web/src/features/evaluation/`
- Create: `apps/web/src/features/export/`
- Create: `apps/web/src/features/jobs/JobDrawer.tsx`
- Test: `apps/web/e2e/evaluate-render.spec.ts`

**Produces:** 四类核心指标、失败解释、配音轨和 MP4 导出。

- [ ] 指标状态区分 ok/not applicable/unavailable/failed，不用 0 混淆。
- [ ] 时长误差在时间线上可见，并有数值文本。
- [ ] 导出提供原声保留、降低和移除模式。
- [ ] 导出完成后提供 WAV、MP4、报告和运行清单入口。
- [ ] 运行桌面与移动只读截图检查。
- [ ] 提交：`feat(web): complete evaluation and export workflow`。

---

## Phase 5：发布、申报与首版验收

### Task 24：制作合法示例与演示项目

**Files:**

- Create: `examples/authorized-demo/`
- Create: `examples/lecture-demo/`
- Create: `examples/ASSET_LICENSES.md`
- Create: `scripts/build_examples.py`
- Test: `tests/e2e/test_examples.py`

**Produces:** 两套不依赖版权电影素材、可重复运行的项目。

- [ ] 录制或生成有明确授权的视频与参考声音，保存书面来源说明。
- [ ] 一套示例突出同角色不同情感；一套示例突出视频节奏和时长同步。
- [ ] 生成低体积代理素材提交仓库，大文件放 Release 并校验哈希。
- [ ] 在干净环境从示例输入生成项目，而不是提交伪造的“成功输出”。
- [ ] 提交：`feat(examples): add redistributable end-to-end dubbing demos`。

### Task 25：完成文档站与模型卡

**Files:**

- Create: `docs/getting-started/`
- Create: `docs/concepts/`
- Create: `docs/adapters/`
- Create: `docs/reference/`
- Create: `docs/governance/`
- Create: `mkdocs.yml`

**Produces:** 中英文快速开始、架构、模型、CLI/API 和贡献文档。

- [ ] 快速开始在干净 GPU Linux 上逐命令验证。
- [ ] 为每个模型写适用场景、输入、显存、语言、限制、许可和引用。
- [ ] 写“从新模型到 Stable”的完整教程。
- [ ] 文档链接检查、命令片段测试和拼写检查进入 CI。
- [ ] 提交：`docs(site): publish reproducible user and adapter guides`。

### Task 26：容器、CI 和供应链

**Files:**

- Create: `deploy/docker/Dockerfile.api`
- Create: `deploy/docker/Dockerfile.worker`
- Create: `deploy/docker/Dockerfile.web`
- Create: `docker-compose.yml`
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/container.yml`
- Create: `.github/workflows/release.yml`
- Create: `.github/workflows/real-model-smoke.yml`

**Produces:** 可构建镜像、自动质量检查、手动 GPU 烟雾测试与 SBOM。

- [ ] 容器使用非 root 用户，权重与项目目录挂载为明确卷。
- [ ] CI 覆盖 Linux Python、Web、Schema、FFmpeg、文档和容器。
- [ ] 真实模型烟雾测试只在受控 GPU runner 手动或发布前触发。
- [ ] 生成 Python/Node/容器 SBOM 与许可证报告。
- [ ] 扫描 secret、依赖漏洞和镜像漏洞，Critical/High 阻断发布。
- [ ] 提交：`ci(release): add reproducible GPU packaging and supply-chain checks`。

### Task 27：完成 `v0.1.0` 质量门

**Files:**

- Modify: `CHANGELOG.md`
- Create: `docs/releases/v0.1.0.md`
- Create: `reports/v0.1.0-validation.md`

**Produces:** 有证据的发布候选，不以文档声称替代真实测试。

- [ ] 执行 `03_EXECUTION/QUALITY_PLAN.md` 的全部自动化、真实模型、视觉和安装验证。
- [ ] 执行 `05_GOVERNANCE/DEFINITION_OF_DONE.md` 的 `v0.1.0` 清单。
- [ ] 在干净 NVIDIA Linux 机器完成 20 分钟快速开始。
- [ ] 完成授权演示的五阶段用户路径与所有导出。
- [ ] 记录硬件、驱动、运行时间、显存和已知限制。
- [ ] 仅在 EmoDubber 或替代核心后端真实支持情感控制后发布“情感可控”表述。
- [ ] 创建签名标签 `v0.1.0`、GitHub Release、镜像、Python 包、SBOM 和校验和。
- [ ] 提交：`release: prepare OpenDub v0.1.0`。

### Task 28：完成基金申报交付

**Files:**

- Modify: `original/青年开源种子计划申报表clean.docx` 的输出副本
- Create: `docs/grant/project-summary.md`
- Create: `docs/grant/demo-script.md`
- Create: `docs/grant/evidence-index.md`

**Produces:** 申报书、演示视频、技术文档和仓库证据一致。

- [ ] 项目仓库只填写 `GalaxyCong/OpenDub`。
- [ ] 在社区贡献中列出既有仓库与真实 Stars/发布状态，并注明“技术基础”而非 OpenDub 已实现模块。
- [ ] 主要功能只写 `v0.1.0` 已实现和资助周期内可验收内容。
- [ ] 演示视频按 `04_OPEN_SOURCE/GRANT_AND_DEMO.md` 录制。
- [ ] 正式影片按 `04_OPEN_SOURCE/DEMO_FILM/README.md`、`MASTER_SCRIPT.md` 与 `TRUTH_AND_QA.md` 执行；申报 alpha 阶段只使用已经真实完成的镜头。
- [ ] 建立申报表每项陈述到仓库文件、Release、测试报告和 Demo 时间码的证据索引。
- [ ] 输出独立 DOCX，不覆盖原始模板；执行 OpenXML 验证和 PDF 视觉检查。
- [ ] 提交：`docs(grant): assemble traceable seed-fund application`。

---

## Phase 6：资助周期扩展

### Task 29：接入 HPMDubbing 视频韵律后端

**Files:**

- Create: `adapters/hpmdubbing/`
- Create: `src/opendub/media/vision/`
- Test: `adapters/hpmdubbing/tests/`
- Test: `tests/integration/models/test_hpmdubbing_pipeline.py`

- [ ] 将脸部检测、口型 ROI、面部情感和场景特征提取改为缓存化组件。
- [ ] 移除硬编码数据路径和人工预处理步骤。
- [ ] 声明精确视频帧率、采样率、hop length 与参考音频要求。
- [ ] 使用授权视频通过完整视频到语音烟雾测试。
- [ ] 与 EmoDubber 在共同输入上比较时长、音色和情感指标，不夸大不共同支持的能力。
- [ ] 提交：`feat(adapter-hpmdubbing): add hierarchical visual prosody backend`。

### Task 30：接入 StyleDubber 风格后端

**Files:**

- Create: `adapters/styledubber/`
- Create: `apps/web/src/features/style/`
- Test: `adapters/styledubber/tests/`
- Test: `apps/web/e2e/style-generation.spec.ts`

- [ ] 定义风格参考的产品级接口，隐藏模型内部多尺度细节。
- [ ] 验证官方权重、数据特征和推理路径。
- [ ] UI 仅在适配器声明支持时显示风格参考和强度。
- [ ] 使用成对样本验证风格参数产生可测变化。
- [ ] 提交：`feat(adapter-styledubber): add multiscale style direction`。

### Task 31：建立研究后端准入流程

**Files:**

- Create: `docs/adapters/research-backend-gate.md`
- Create: `model-registry/planned/`
- Test: `tests/unit/model_registry/test_maturity_gate.py`

- [ ] 为 HD-Dub、CoSyncDiT、LLM-Flow-Dubber 建立独立准入记录。
- [ ] 只有代码、权重、许可证、输入协议和真实测试齐全才从 Planned 升为 Experimental。
- [ ] 不将论文录用或 Demo 页面等同于可集成代码。
- [ ] 为 Experimental 到 Stable 设置相同契约测试，不建立“内部模型例外”。
- [ ] 提交：`docs(models): formalize research backend promotion gates`。

### Task 32：制作并验证 OpenDub 正式演示影片

**Files:**

- Create: `demo-film/` 的受控剪辑工程和素材登记
- Create: `docs/releases/demo-film-validation.md`
- Create: `docs/releases/demo-film-evidence-index.md`
- Release: `OpenDub_DemoFilm_2m40_CN_ENSub.mp4`
- Release: `OpenDub_Teaser_60s.mp4`
- Release: `OpenDub_Loop_30s_Muted.mp4`

**Interfaces:**

- Consumes: 授权示例项目、Stable Adapter、指标报告、运行清单、公开仓库和 `TODO/04_OPEN_SOURCE/DEMO_FILM/` 制作包。
- Produces: 可被申报、README、路演和社交媒体复用的、具有证据索引的成片与派生版本。

- [ ] 根据 `ASSET_AND_RIGHTS.md` 为每一项画面、声音、音乐、字体和上游截图登记来源与发布权利。
- [ ] 锁定一个可从当前 OpenDub 版本实际复现的演示项目，生成普通朗读、真实不匹配候选和确认候选三条公平对比音频。
- [ ] 按 `RECORDING_RUNBOOK.md` 录制实拍素材、Studio 主路径、精确 UI 镜头、指标与开源证据。
- [ ] 按 `MASTER_SCRIPT.md` 制作 2 分 40 秒正式版，A/B 段落留出纯听觉空间，不用音乐或后期声音美化干扰对比。
- [ ] 按 `POST_PRODUCTION.md` 输出带旁白、无旁白、60 秒、30 秒、字幕和 PNG 片尾；所有导出文件由 FFprobe 检查格式、帧率、音频采样率和时长。
- [ ] 由技术负责人、非项目成员和声音审查者按 `TRUTH_AND_QA.md` 审查；所有阻断问题重录或重剪。
- [ ] 建立影片时间码到运行报告、模型版本、指标和素材授权的证据索引。
- [ ] 提交：`docs(demo): release verified OpenDub product film`。

## 实施结束条件

只有 Task 1–28 全部完成，且真实情感控制后端通过验证，项目才达到本次申报与 `v0.1.0` 目标。Task 29–31 是资助周期内的模型扩展路线；Task 32 是正式演示影片发布门。它们不阻塞首版代码发布，但其状态必须在 README 和申报书中如实展示。
