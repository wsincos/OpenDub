# OpenDub Method Atlas Implementation Master Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement the linked plans task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 OpenDub `v0.0.1-alpha.0` 基础上完成任务优先、三种完整方法可视化、同输入比较和可选 Live 运行的申报版本。

**Architecture:** React 静态 Atlas 负责无需 GPU 的 Concept 和 Replay 体验；现有 FastAPI、媒体管线和隔离 Adapter Runtime 负责可选 Live。内容由 Method、Case、Replay 和 Signal 四类版本化 manifest 驱动，三种方法只共享外围协议。

**Tech Stack:** Python 3.11+、Pydantic v2、FastAPI、Typer、React 19、TypeScript、Vite、React Router、Zustand、React Flow、ELK、uPlot、Canvas/Web Audio、Vitest、Testing Library、Playwright、pytest、FFmpeg。

## Global Constraints

- 三套方法为 HPMDubbing、StyleDubber、EmoDubber，不跨方法拼接内部模块。
- Concept/Replay 必须在没有 API、GPU 和 checkpoint 时可使用。
- 内容状态使用 `concept`、`replay`、`live`、`planned`；运行状态另行记录。
- 时间统一使用整数微秒；音频精确位置使用整数 sample。
- 示意数值必须 `illustrative=true`，不得进入指标或方法比较。
- Replay 和 Live 资产必须有 SHA-256、来源和权利记录。
- 公开内容只使用自制、公共领域或有明确展示和分发许可的素材。
- 方法事实来自原论文和固定源码提交，不从二手博客复制。
- 前端不硬编码方法图、案例结果和状态。
- 每项任务遵循失败测试、最小实现、通过测试、文档检查、独立提交。

---

## 当前基础

已经完成且不重复实现：

- Python 领域模型、项目存储、媒体探测和 FFmpeg 渲染。
- Model Registry、权重校验、隔离运行时和可恢复任务管线。
- FastAPI、CLI、本地 Web Studio。
- 授权记录、候选结果、基础评测和导出 manifest。
- 89 项自动化测试通过的 alpha 基线。

现有 Studio 先迁移到 `/studio`，其业务行为保持不变。Atlas 完成后再对 Studio 进行视觉整合。

## 子项目和顺序

### M1：Task Explorer

执行 [01_TASK_EXPLORER_PLAN.md](01_TASK_EXPLORER_PLAN.md)。

交付：

- Atlas Schema 和内容 SDK。
- 应用路由与新 Shell。
- 全局时间控制器。
- 视频、文本、参考语音和输出的交互式任务解释。
- 响应式和无障碍首屏。

入口门槛：当前 alpha `make check` 通过。
出口门槛：无 API 模式下 `/explore` 完整可用。

### M2：Three Complete Method Canvases

执行 [02_METHOD_ATLAS_PLAN.md](02_METHOD_ATLAS_PLAN.md)。

交付：

- 三套经过校验的 Method Manifest。
- 方法演进 Atlas。
- React Flow Method Canvas。
- 可点击组件检查器和信号台。
- HPM、Style、Emo 三种方法专属 Concept 交互。
- Evidence Room。

入口门槛：M1 内容 SDK、路由和时间控制器稳定。
出口门槛：三个方法页均能从论文问题进入组件、信号和证据。

### M3：Comparison Lab

执行 [03_COMPARISON_LAB_PLAN.md](03_COMPARISON_LAB_PLAN.md)。

交付：

- Case 和 Replay Bundle 工具链。
- 授权共同案例。
- 同步 A/B/C 播放和盲听。
- 共同指标与不适用状态。
- 可导出的比较报告。

入口门槛：至少两个方法有合法 Replay 结果；如果只有一个结果，先完成工具链和单结果 UI，不发布伪比较。
出口门槛：同输入比较可追溯、可复现、不会发生叠音。

### M4：Content, Live and Grant Delivery

执行 [04_LIVE_AND_CONTENT_PLAN.md](04_LIVE_AND_CONTENT_PLAN.md)。

交付：

- 三方法内容作者核验。
- 完整授权 Replay 内容包。
- 条件允许时至少一个 Live Adapter 与 VisualizationProvider。
- Evidence Room 最终状态。
- 申报影片和发布证据包。

入口门槛：M1 至 M3 的静态产品通过 QA。
出口门槛：申报片中每个画面与发布版本一致，所有状态真实。

## 发布序列

| Tag | 内容 | 是否依赖 checkpoint |
|---|---|---:|
| `v0.1.0-atlas-rc1` | Task Explorer + 三套 Concept Canvas | 否 |
| `v0.1.0-atlas-rc2` | 授权 Replay + Comparison Lab | 否，但依赖合法结果视频 |
| `v0.1.0-atlas` | 申报内容、Evidence、正式影片 | 否 |
| `v0.2.0-live` | 至少一套真实模型现场生成 | 是 |

如果 checkpoint 在申报截止前无法满足许可和复现门槛，发布 `v0.1.0-atlas`，影片明确使用 Replay。不得为追求 Live 标签降低真实性要求。

## 全量验收命令

```bash
uv sync --all-groups
pnpm install --frozen-lockfile
uv run opendub atlas validate content
uv run pytest -q
pnpm --filter @opendub/web test -- --run
pnpm --filter @opendub/web build
pnpm --filter @opendub/web exec playwright test
uv run python scripts/check_docs_links.py
git diff --check
```

预期：

- Python 和 Web 测试全部通过。
- 三套方法 manifest、案例和 Replay 无 Schema、hash 或 rights 错误。
- 五个目标视口没有文字遮挡、空白图谱或时间轴错位。
- 未就绪的 Live 功能保持禁用并说明原因。
