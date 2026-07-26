# Documentation and Community Plan

## README 结构

README 首屏应在一个桌面视口内完成：

1. OpenDub 名称和一句话定位；
2. 一张真实 Studio 截图或授权演示短 GIF；
3. 三套完整方法的 `Concept` / `Replay` / `Live` 内容与运行状态；
4. “探索方法”和“创建本地项目”两个入口；
5. Apache-2.0、Python、CI 状态。

后续顺序：

- Why OpenDub；
- Atlas、方法选择与本地项目准备的真实功能列表；
- `理解 -> 选择 -> 准备 -> 条件运行` 工作流；
- 快速开始；
- 模型能力表；
- 示例；
- 架构；
- Roadmap；
- Responsible use；
- Citation；
- Contributing；
- License。

README 不能把 Planned 模型列为已支持。

## 文档站

### Getting Started

- 系统要求；
- 无 GPU 的 Atlas 与本地项目快速开始；
- 原生 uv 安装；
- 创建第一个授权项目并选择完整方法；
- 条件运行：下载并接受已验证模型权重条款；
- 常见故障。

### Concepts

- 为什么视频配音不同于 TTS；
- 项目、角色、参考声音、片段和候选；
- 情感与风格；
- 视觉同步；
- 模型能力与成熟度；
- 指标解释；
- 本地数据与授权。

### Adapter SDK

- 最小 TestAdapter；
- 能力声明；
- 环境检查；
- 输入准备；
- 隔离进程；
- 权重管理；
- 错误映射；
- 契约测试；
- 模型卡；
- Stable 准入。

### Reference

- CLI；
- REST API；
- Project Schema；
- Run Schema；
- 配置；
- 环境变量；
- 目录；
- 错误码。

### Governance

- Roadmap；
- 模型状态；
- 安全；
- 许可；
- 负责任使用；
- 发布流程；
- 决策记录。

## 中英文策略

- README、快速开始、负责任使用、贡献指南和主要 Demo 提供中英文。
- API、代码、Schema 和错误码使用英文。
- UI 首版支持中文与英文文案，文案 key 固定。
- 模型论文原名不翻译，功能名称可以双语。

## Issue 体系

初始标签：

- `area:core`
- `area:web`
- `area:media`
- `area:adapter`
- `area:metrics`
- `area:docs`
- `model:emodubber`
- `model:hpmdubbing`
- `model:styledubber`
- `kind:bug`
- `kind:feature`
- `kind:adapter`
- `kind:good-first-issue`
- `status:needs-reproduction`
- `status:blocked-upstream`
- `priority:p0` 至 `priority:p3`

初始公开 Issue 至少包括：

1. 三方法 Atlas 语义复核；
2. Atlas 到 Studio 的方法选择记录；
3. 授权示例素材；
4. 项目 Schema；
5. FFmpeg 媒体管线；
6. Web Studio 已选方法与输入契约；
7. 合格 Replay Bundle；
8. 第一套方法的 Live 准入审计；
9. Docker GPU；
10. 中英文快速开始。

## 贡献流程

1. Issue 对齐范围；
2. Fork 和短分支；
3. 先写或更新测试；
4. 运行 `make check`；
5. 更新模型卡、文档和 NOTICE；
6. 提交 PR；
7. 维护者检查功能、许可、复现和安全；
8. Adapter 首次只能进入 Experimental；
9. 真实测试和使用反馈满足后单独 PR 升级 Stable。

## 模型卡标准

每个模型卡必须包含：

- 概述和论文；
- OpenDub 中的功能；
- 支持输入、语言和控制；
- 权重和许可；
- 推理硬件；
- 测试环境；
- 指标；
- 已知限制；
- 不适用场景；
- 数据与伦理；
- 引用。

## 社区运营

资助周期内：

- 每两周发布一次开发进展；
- 每个月一个可运行 milestone；
- 维护公开 Roadmap；
- 48 小时内初步回应阻断 Issue；
- 发布至少一篇从论文代码到 Adapter 的技术文章；
- 举办一次线上演示或开发者交流；
- 收集安装成功率、文档问题、外部 PR 和真实应用反馈。

不使用 Stars 作为唯一成功指标。更重要的指标是：

- 独立用户成功运行示例；
- 有效 Issue；
- 外部 PR；
- 新 Adapter；
- Release 下载；
- 文档任务完成率；
- 真实应用案例。

## 引用与学术归属

- 根目录 `CITATION.cff` 引用 OpenDub 平台；
- 模型卡引用对应论文；
- 报告自动输出所用模型 BibTeX；
- OpenDub 论文/文档不能把各模型贡献统一改写为平台原创；
- 上游贡献者和团队成员按实际贡献记录。
