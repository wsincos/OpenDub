# OpenDub Planning Hub

本目录是 OpenDub 后续设计、实现、申报和演示的唯一规划入口。当前规划已经完成一次方向重构：

- 不把 HPMDubbing、StyleDubber、EmoDubber 的内部模块拆散后重新拼成一个模型。
- 不把若干论文仓库简单排列成成果目录。
- 将三项团队原创方法保留为三套完整的视频配音生成方法。
- 由 OpenDub 提供统一任务解释、交互式方法可视化、同输入结果比较、复现信息和可选 Live 运行。

当前代码仓库已经具有 `v0.0.1-alpha.0` 的项目、媒体、任务、API、CLI 和 Studio 基础。新规划以这些可验证能力为底座，建设申报版本的核心产品：

> **OpenDub Method Atlas：面向视频配音生成的交互式方法图谱、可视化解释与统一比较平台。**

## 最高优先级结论

### 申报项目形式

本次只申报一个项目和一个主仓库：

- 项目名称：`OpenDub`
- 中文全称：`OpenDub 视频配音生成交互式方法图谱与开源平台`
- 英文副标题：`Interactive Atlas for Visual Dubbing`
- 主仓库：`https://github.com/wsincos/OpenDub`
- 申报方向：`AIGC 应用与工具`
- 新增平台代码许可证：`Apache-2.0`

### 首版核心方法

首个申报版本只包含三套核心视频配音方法：

1. `HPMDubbing`：分层视觉韵律建模。
2. `StyleDubber`：多尺度风格学习。
3. `EmoDubber`：高质量、用户情感可控的电影配音。

`HPMDubbing_Vocoder` 是支持性声学生成基础设施，不作为第四套同级配音方法。其他 GalaxyCong 仓库只进入 `Supporting`、`Reference` 或 `Planned` 区域，不能与三套核心方法并列声称已经接入。

### 产品主线

```text
Task Explorer
    解释 Video + Text + Reference Speech -> Dubbed Speech
        |
        v
Method Atlas
    选择一套完整方法
        |
        v
Method Canvas
    点击组件、跟随数据流、检查时间对齐信号
        |
        v
Comparison Lab
    在同一输入下并排试听、观察和比较
        |
        v
Studio / Live
    在许可与权重齐备时执行真实模型并导出成片
```

## 实施时必须遵守的五条规则

1. **完整方法规则**：三套论文方法各自独立运行，不跨方法抽取内部模块组成新模型。
2. **任务准确规则**：研究任务输出是目标配音语音，OpenDub 产品再将其与视频混流得到成片。
3. **状态诚实规则**：所有展示必须标记 `Concept`、`Replay`、`Live` 或 `Planned`。
4. **可视化有据规则**：只展示论文定义、代码导出或离线预计算得到的信号，不制造无语义的“神经网络动画”。
5. **比较公平规则**：同一输入、同一裁剪、同一音量规则、同一时间轴和共同适用指标下才允许横向比较。

## 阅读顺序

### 产品定义

1. [项目章程](00_PRODUCT/PROJECT_CHARTER.md)
2. [视频配音任务定义](00_PRODUCT/TASK_DEFINITION.md)
3. [Method Atlas 产品规格](00_PRODUCT/METHOD_ATLAS_SPEC.md)
4. [产品与视觉体验](00_PRODUCT/PRODUCT_EXPERIENCE.md)
5. [范围与成功标准](00_PRODUCT/SCOPE_AND_SUCCESS.md)
6. [用户工作流](00_PRODUCT/USER_WORKFLOWS.md)

### 方法与内容

7. [方法与模型映射](01_CAPABILITIES/CAPABILITY_AND_MODEL_MAP.md)
8. [三套方法内容规格](01_CAPABILITIES/CORE_METHODS.md)
9. [可视化信号清单](01_CAPABILITIES/VISUALIZATION_SIGNAL_MAP.md)
10. [上游基线](01_CAPABILITIES/UPSTREAM_BASELINE.md)

### 技术设计

11. [系统架构](02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)
12. [Atlas 数据契约](02_ARCHITECTURE/ATLAS_CONTRACTS.md)
13. [已有领域契约](02_ARCHITECTURE/DOMAIN_CONTRACTS.md)
14. [仓库结构](02_ARCHITECTURE/REPOSITORY_LAYOUT.md)
15. [安全、许可与伦理](02_ARCHITECTURE/SAFETY_LICENSING.md)

### 执行计划

16. [执行总纲](03_EXECUTION/IMPLEMENTATION_PLAN.md)
17. [任务解释器计划](03_EXECUTION/01_TASK_EXPLORER_PLAN.md)
18. [方法图谱计划](03_EXECUTION/02_METHOD_ATLAS_PLAN.md)
19. [比较实验室计划](03_EXECUTION/03_COMPARISON_LAB_PLAN.md)
20. [Live 运行与内容计划](03_EXECUTION/04_LIVE_AND_CONTENT_PLAN.md)
21. [质量计划](03_EXECUTION/QUALITY_PLAN.md)
22. [当前实现状态](03_EXECUTION/STATUS.md)

### 申报与演示

23. [申报叙事与交付物](04_OPEN_SOURCE/GRANT_AND_DEMO.md)
24. [申报冲刺](04_OPEN_SOURCE/APPLICATION_FAST_TRACK.md)
25. [演示影片制作包](04_OPEN_SOURCE/DEMO_FILM/README.md)
26. [CNN 可视化参考转译](06_REFERENCE/CNN_VISUALIZATION_TRANSLATION.md)

### 治理

27. [决策与风险](05_GOVERNANCE/DECISIONS_AND_RISKS.md)
28. [完成定义](05_GOVERNANCE/DEFINITION_OF_DONE.md)
29. [追踪矩阵](05_GOVERNANCE/TRACEABILITY_MATRIX.md)

## 后续启动方式

后续收到“开始实现”指令时，严格按照以下顺序执行：

1. 读取 [当前实现状态](03_EXECUTION/STATUS.md)，确认工作树和依赖。
2. 执行 [任务解释器计划](03_EXECUTION/01_TASK_EXPLORER_PLAN.md)。
3. 执行 [方法图谱计划](03_EXECUTION/02_METHOD_ATLAS_PLAN.md)。
4. 执行 [比较实验室计划](03_EXECUTION/03_COMPARISON_LAB_PLAN.md)。
5. 根据 checkpoint 和素材可用性执行 [Live 运行与内容计划](03_EXECUTION/04_LIVE_AND_CONTENT_PLAN.md)。
6. 完成申报影片和证据包，运行全量验收。

任何范围变化先记录到 [决策与风险](05_GOVERNANCE/DECISIONS_AND_RISKS.md)，再修改对应规格。不得直接以临时代码改变产品定义。
