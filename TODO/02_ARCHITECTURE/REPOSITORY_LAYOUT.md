# Repository Layout

## 顶层结构

```text
OpenDub/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   ├── CODEOWNERS
│   └── pull_request_template.md
├── apps/
│   └── web/
├── src/
│   └── opendub/
├── adapters/
│   ├── emodubber/
│   ├── hpmdubbing/
│   ├── styledubber/
│   └── hpm_vocoder/
├── schemas/
├── tests/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── examples/
│   ├── authorized-demo/
│   └── lecture-demo/
├── docs/
│   ├── getting-started/
│   ├── concepts/
│   ├── adapters/
│   ├── reference/
│   └── governance/
├── deploy/
│   └── docker/
├── scripts/
├── licenses/
├── model-registry/
├── pyproject.toml
├── uv.lock
├── package.json
├── pnpm-workspace.yaml
├── docker-compose.yml
├── LICENSE
├── NOTICE
├── CITATION.cff
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── README.md
```

## Python 包

```text
src/opendub/
├── __init__.py
├── config.py
├── domain/
│   ├── ids.py
│   ├── time.py
│   ├── project.py
│   ├── assets.py
│   ├── segments.py
│   ├── candidates.py
│   ├── jobs.py
│   ├── metrics.py
│   ├── errors.py
│   └── transitions.py
├── application/
│   ├── project_service.py
│   ├── ingest_service.py
│   ├── generation_service.py
│   ├── evaluation_service.py
│   ├── render_service.py
│   └── doctor_service.py
├── storage/
│   ├── project_store.py
│   ├── artifact_store.py
│   ├── sqlite_index.py
│   └── atomic.py
├── media/
│   ├── probe.py
│   ├── ffmpeg.py
│   ├── proxy.py
│   ├── audio.py
│   ├── waveform.py
│   ├── timeline.py
│   └── render.py
├── models/
│   ├── capabilities.py
│   ├── protocols.py
│   ├── registry.py
│   ├── manifests.py
│   ├── weights.py
│   ├── runtime.py
│   └── subprocess_worker.py
├── pipeline/
│   ├── stages.py
│   ├── cache.py
│   ├── planner.py
│   ├── executor.py
│   └── cancellation.py
├── evaluation/
│   ├── protocols.py
│   ├── registry.py
│   ├── content.py
│   ├── speaker.py
│   ├── emotion.py
│   ├── sync.py
│   ├── audio_quality.py
│   └── report.py
├── jobs/
│   ├── models.py
│   ├── repository.py
│   ├── scheduler.py
│   └── events.py
├── api/
│   ├── app.py
│   ├── dependencies.py
│   ├── errors.py
│   ├── schemas.py
│   └── routes/
├── cli/
│   ├── app.py
│   ├── output.py
│   └── commands/
└── observability/
    ├── logging.py
    ├── redaction.py
    └── diagnostics.py
```

每个文件只承担一个明确职责。领域层禁止导入 `api`、`media`、`models` 和外部框架。

## 模型适配器包

```text
adapters/emodubber/
├── pyproject.toml
├── README.md
├── MODEL_CARD.md
├── LICENSES.md
├── adapter.yaml
├── src/opendub_adapter_emodubber/
│   ├── __init__.py
│   ├── adapter.py
│   ├── environment.py
│   ├── inputs.py
│   ├── runner.py
│   └── outputs.py
└── tests/
    ├── test_capabilities.py
    ├── test_inputs.py
    ├── test_contract.py
    └── test_real_smoke.py
```

适配器不直接复制上游整个仓库。优先采用：

1. 明确提交版本的依赖；
2. 独立补丁文件；
3. 最小必要兼容层；
4. 无法避免复制时保留原许可证、版权头和来源说明。

## Web Studio

```text
apps/web/src/
├── app/
│   ├── router.tsx
│   ├── providers.tsx
│   └── shell/
├── features/
│   ├── projects/
│   ├── assets/
│   ├── player/
│   ├── timeline/
│   ├── segments/
│   ├── voices/
│   ├── emotion/
│   ├── models/
│   ├── candidates/
│   ├── jobs/
│   ├── evaluation/
│   └── export/
├── components/
│   ├── ui/
│   └── layout/
├── api/
│   ├── client.ts
│   ├── generated/
│   └── events.ts
├── store/
├── styles/
│   ├── tokens.css
│   └── globals.css
├── test/
└── main.tsx
```

按产品功能组织前端，避免按“pages/components/utils”形成超大通用目录。OpenAPI 生成 API 类型，前端不手写重复 DTO。

## 配置与状态路径

遵循 XDG：

- 配置：`$XDG_CONFIG_HOME/opendub/config.toml`
- 数据：`$XDG_DATA_HOME/opendub/`
- 缓存：`$XDG_CACHE_HOME/opendub/`
- 状态：`$XDG_STATE_HOME/opendub/`

环境变量统一使用 `OPENDUB_` 前缀。测试必须使用临时目录，不能读取开发者真实用户目录。

## 依赖选择

### Python

- Python `>=3.11`
- `uuid6`：生成 UUIDv7 领域标识
- `pydantic` v2：配置和 API Schema
- `fastapi`：本地 API
- `typer` + `rich`：CLI
- `sqlalchemy` + SQLite：索引与任务状态
- `httpx`：模型清单和下载
- `soundfile` / `numpy`：音频 I/O 与基础处理
- `torch`：仅在需要的适配器或指标环境中安装
- `pytest`、`ruff`、`mypy`：质量工具

### Web

- React + TypeScript + Vite
- TanStack Query：服务端状态
- Zustand：纯 UI/编辑会话状态
- Radix primitives：可访问交互
- Lucide：图标
- WaveSurfer：波形
- Vitest + Testing Library
- Playwright：端到端

核心包避免依赖 PyTorch，使不具备 GPU 的用户也能编辑项目、查看报告和运行媒体工具。

## 命名

- Python 模块、CLI 参数、JSON 字段：`snake_case`
- TypeScript 变量：`camelCase`
- React 组件：`PascalCase`
- API 路径：复数名词和 kebab-case
- Adapter ID：`publisher/model-name`
- Metric ID：`category.metric_name`
- Git 分支：`feat/`、`fix/`、`docs/`、`release/`

## Git 提交

采用 Conventional Commits：

- `feat(core): add project manifest validation`
- `feat(adapter-emodubber): add generation runtime`
- `fix(media): preserve exact output duration`
- `docs(adapter): document capability contract`
- `test(e2e): cover authorized demo workflow`

每个实施任务结束时形成一个可评审提交，不将生成权重、用户素材、缓存和本地日志提交到 Git。
