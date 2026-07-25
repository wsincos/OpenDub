# OpenDub Implementation Status

**Last updated:** 2026-07-26
**Repository state:** `v0.0.1-alpha.0` foundation complete; public Concept Atlas first slice implemented and under evidence review.
**Planning source:** [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)

## 已完成的真实基础

| 区域 | 已验证能力 |
|---|---|
| 治理与来源 | Apache-2.0 平台治理、固定上游提交、上游审计、权重准入规则 |
| 项目与媒体 | project.json、原子存储、FFprobe/FFmpeg、字幕、时间线、混流和导出 manifest |
| 授权 | 参考声音来源与分发许可记录 |
| 运行基础 | 模型能力契约、权重 hash、隔离运行时、任务和可恢复流水线 |
| 评测 | 时长、静音、削波等确定性指标；不可用神经指标明确标记 |
| API/CLI | 项目、素材、片段、候选、评测、渲染、任务事件 |
| Web Studio | 本地项目列表、媒体导入、授权、片段、时间线、候选和导出 |
| 文档与申报 | 现有申报表草案、证据索引、上游审计 |
| 自动化 | 最近一次记录为 89 tests passing；正式启动前重新运行确认 |

## 新方向已完成的规划

- Task-first 的视频配音任务定义。
- HPMDubbing、StyleDubber、EmoDubber 三套完整方法范围。
- Concept、Replay、Live、Planned 内容状态。
- Method Manifest、Case、Replay、Signal 数据契约。
- Method Canvas、Comparison Lab、Evidence Room 产品设计。
- 四份按测试和提交边界拆分的实施计划。
- 申报影片新的任务解释和方法可视化主线。

## 尚未实现

| 能力 | 当前状态 | 下一证据 |
|---|---|---|
| `/explore` Task Explorer | Concept 页面、输入/输出解释、时间线和方法入口已实现 | 真实案例与 E2E |
| 三套 Method Manifest | 3 份结构化 manifest 已通过 `opendub atlas validate` | 论文作者或负责人语义复核 |
| 三套 Method Canvas | 总览、三张可点击 Concept 画布和 Signal Dock 已实现 | manifest 驱动布局、真实或授权信号 |
| 合法 Replay Bundle | 尚未选定 | 素材/声音权利审计和 hash |
| 同输入 Comparison Lab 内容 | 证据门控界面已实现；没有公开 replay 结果 | 至少两个方法对同一输入的合法输出 |
| Live Emo/HPM/Style | unavailable；已发现若干待审计 Drive 候选 | 明确许可的 checkpoint、hash、真实 smoke |
| VisualizationProvider | 契约已规划 | 一套真实 Adapter 的中间产物 |
| 新申报影片 | 脚本规划中 | 固定发布版本的 UI 录制与事实核验 |

## checkpoint 对项目进度的影响

- **不需要 checkpoint**：Task Explorer、三套 Concept Canvas、论文与代码 Evidence、方法专属合法历史 Demo Replay。
- **可能需要 checkpoint**：生成同一输入的多方法结果。
- **必须需要 checkpoint**：修改输入后的现场 Live 生成、真实中间产物捕获。

因此下一动作不是等待 checkpoint，而是完成 Concept 内容的权利记录、manifest 驱动客户端和作者复核，再审计可公开 Replay。候选详情见 `docs/atlas/checkpoint-audit-2026-07-26.md`。

## 下一执行顺序

1. 完成 Concept 资产权利记录和 manifest 驱动客户端。
2. 进行三套方法的论文/代码语义复核。
3. 审计并打包可公开 Replay。
4. 只有通过相同输入门槛才解锁 Comparison Lab 的试听、信号和指标。
5. checkpoint 条件满足后再升级一套方法为 Live。

## 真实性规则

当前任何研究模型都不能标为 Live。测试用正弦波和合成媒体只能作为自动化 fixture，不得出现在公开方法结果、申报片或“模型生成”叙事中。
