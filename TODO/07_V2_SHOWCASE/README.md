# OpenDub V2 展示重构总览

**状态：** 网页、案例资产与申报片初版已实施；正在进行最终 QA、独立严格审查和发布收口。
**目标版本：** `v2.0.0-showcase`，独立于已发布的 `v0.0.1-alpha.0`。
**定位：** 把 OpenDub 的第一印象从“研究工作台录屏”升级为“可进入、可理解、可验证的 VTTS 任务体验”，并以真实、可追溯的样例证明团队已有方法成果。

## 1. 本轮为什么需要重构

V1 已经证明了平台逻辑：任务解释、三种完整方法、选择引导、Studio 和 Evidence Room 能形成可信闭环。但 V1 视频主要由静态网页镜头组成，首屏的 `Input Conditions -> Complete Dubbing Method -> Output` 缺少明确的数据流动、真实媒体质感和样例结果锚点。

V2 的目标不是把页面改成泛化的“AI 科技风”，更不是将未验证内容包装成 Live。它要完成三件具体的事：

1. 在进入 Atlas 前，用动态 VTTS 任务舞台清楚解释“无声视频、目标台词、授权参考语音如何共同约束目标语音”；
2. 将已提供的真人与动画 GT / HPMDubbing / StyleDubber / EmoDubber 视频做成可追溯样例展台；
3. 用一部重新制作的、动态且可核查的申报视频，把任务、成果、方法选择和证据边界串成一条叙事。

实施记录见 [06_IMPLEMENTATION_RECORD.md](06_IMPLEMENTATION_RECORD.md)。它是本总览与各计划文档之间的当前事实来源；计划中的长期目标并不自动成为已发布能力。

## 2. 设计结论

采用 **Cinematic VTTS Atlas（电影化 VTTS 任务图谱）**，而不是营销式落地页或背景动画：

```text
V2 first route: /vtts
  Animated VTTS task stage
      -> synchronized cue microscope
      -> verified example gallery
      -> /explore and /methods
      -> existing Studio / Evidence workflow
```

- `/vtts` 是产品功能入口，不是脱离应用的宣传页；用户可逐项暂停、检查输入、切换案例、进入完整方法。
- 动画使用 SVG、Canvas 或 Web Animations API 解释真实的数据依赖：沿路径推进的信号、时间游标、音素片段和由真实音频计算的特征。
- V2 保留现有 Task Explorer、Method Atlas、Canvas、Studio、Evidence 和 Compare 的真实边界。V1 仍可通过 tag `v0.0.1-alpha.0` 复核。

## 3. 不可违反的边界

| 内容 | V2 允许的表述 | 禁止的表述 |
| --- | --- | --- |
| VTTS 动态流程图 | 任务定义、输入约束、完整方法接口 | “OpenDub 此刻正在生成” |
| GT / 三方法视频 | 已归档样例、方法署名、case 级来源 | 未经核验就称公平 benchmark、Replay 或 Live run |
| 真实波形、mel、F0 | 由同一已授权 GT 音频离线提取，标示 case 和来源 | 随机生成后称真实信号 |
| 文字 / IPA | 有 canonical record 时展示 case 级标注；当前无记录的历史样例只展示明确标记的任务示意 | 把任务示意伪称为样例的真实转写或对齐 |
| 方法选择 | “适合优先理解 / 准备” | “自动选择最佳模型” |
| 音频播放 | 单独显示资产来源和内容状态 | 将旁白、GT 或旧结果说成新的生成输出 |

`Replay` 只用于来源、输入合同、权利、方法 revision、输出哈希全部齐备的案例。其余可展示的历史样例一律标为 `Archived research example`，不进入公平比较或 Live 能力声明。

## 4. 执行顺序

1. [反馈与验收要求](00_FEEDBACK_AND_REQUIREMENTS.md)：确认 V2 的用户可见目标和不做事项。
2. [VTTS 视觉与交互规格](01_VTTS_VISUAL_AND_INTERACTION_SPEC.md)：先锁定动画、布局、状态与无障碍规则。
3. [样例与信号资产计划](02_EXAMPLE_EVIDENCE_AND_ASSET_PLAN.md)：先建立版权、来源、哈希和特征资产，再把任何视频放入页面。
4. [网页实施清单](03_WEB_V2_IMPLEMENTATION_PLAN.md)：按测试先行实现 `/vtts`、真实信号和样例展台。
5. [视频重制方案](04_FILM_V2_PRODUCTION_PLAN.md)：在网页稳定后录制 V2，而不是先剪辑一部脱离网页的宣传片。
6. [质量、发布与复审](05_V2_QUALITY_RELEASE_AND_AUDIT.md)：完成视觉、内容、视频和远端发布验证后，进行严格复审。

## 5. V2 完成定义

只有同时满足以下事实，才可标记为 `v2.0.0-showcase`：

- 首次进入 `/vtts` 的用户在 20 秒内能说清三类输入、完整方法和两个输出；
- 数据流图具有可暂停的、可解释的运动，而非仅有装饰性循环；
- `Face`、`Lip`、`Environment` 三类视觉线索都可查看，时间线上存在真实 GT 波形和真实声学图；IPA 仅在拥有 canonical record 时作为 case 标注，当前页面 IPA 为明确的任务示意；
- 真人与动画两组样例均有 GT、三种方法、内容状态、来源、哈希和播放策略；
- 当前两组案例因缺少 canonical transcript / IPA 合同，保持 `Archived research example` 且不可作为真实 IPA 时间线或 Replay 比较；
- V2 视频在 84 秒内展示真实浏览器动态任务、真实样例、方法选择和证据边界，且没有错误的 Live / Replay 声称；
- 自动化测试、生产构建、媒体完整性检查、桌面/移动端视觉 QA、视频与申请材料审计全部通过；
- 源码、资产 manifest、V2 视频和审核报告被发布到可引用 tag；V1 交付物不被覆盖。
