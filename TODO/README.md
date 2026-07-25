# OpenDub Planning Hub

本目录是 OpenDub 从零建设的唯一规划入口。它定义项目定位、产品体验、模型能力边界、系统架构、实施顺序、质量门槛、开源治理和申报交付物。后续实现应以这里的文档为准；若实现中需要改变已定设计，先在 `05_GOVERNANCE/DECISIONS_AND_RISKS.md` 记录决策，再同步修改受影响的规格和任务。

## 项目结论

- 官方名称：**OpenDub**
- 中文名称：**OpenDub 多模态情感可控视频配音工具**
- 一句话定位：从视频画面理解角色状态，在给定台词和授权参考声音的条件下，生成音色一致、情感可控、节奏匹配、可直接回填视频的配音。
- 首个公开版本：`v0.1.0`
- 申报方向：`AIGC 应用与工具`
- 主仓库：`https://github.com/GalaxyCong/OpenDub`
- 新增平台代码许可证：`Apache-2.0`
- 首发平台：Linux + NVIDIA CUDA；CPU 支持媒体预处理、项目编辑和结果查看，不承诺 CPU 完成神经配音生成。
- 核心区别：OpenDub 不是普通文本转语音，也不是论文代码集合；它围绕“视频感知、角色一致、情感可控、时间同步”提供完整创作工作流。

## 阅读顺序

1. [项目章程](00_PRODUCT/PROJECT_CHARTER.md)：为什么做、为谁做、什么不做。
2. [范围与成功标准](00_PRODUCT/SCOPE_AND_SUCCESS.md)：`v0.1.0` 的硬边界和验收指标。
3. [产品与视觉体验](00_PRODUCT/PRODUCT_EXPERIENCE.md)：品牌、界面、交互与文案规范。
4. [用户工作流](00_PRODUCT/USER_WORKFLOWS.md)：创作者和开发者如何完成任务。
5. [能力与模型映射](01_CAPABILITIES/CAPABILITY_AND_MODEL_MAP.md)：每个已有仓库在 OpenDub 中对应什么功能。
6. [上游基线](01_CAPABILITIES/UPSTREAM_BASELINE.md)：当前公开仓库的可接入证据和限制。
7. [系统架构](02_ARCHITECTURE/SYSTEM_ARCHITECTURE.md)：组件边界和运行方式。
8. [领域契约](02_ARCHITECTURE/DOMAIN_CONTRACTS.md)：项目、片段、声音、任务、结果和模型适配接口。
9. [仓库结构](02_ARCHITECTURE/REPOSITORY_LAYOUT.md)：未来代码应落在哪些目录。
10. [安全、许可与伦理](02_ARCHITECTURE/SAFETY_LICENSING.md)：声音授权、素材版权、模型许可和滥用防护。
11. [总实施计划](03_EXECUTION/IMPLEMENTATION_PLAN.md)：按依赖顺序从零实现。
12. [测试与质量](03_EXECUTION/QUALITY_PLAN.md)：测试矩阵、性能指标与发布门槛。
13. [发布与运维](03_EXECUTION/RELEASE_OPERATIONS.md)：模型制品、版本、CI/CD 和故障诊断。
14. [文档与社区](04_OPEN_SOURCE/DOCUMENTATION_COMMUNITY.md)：README、教程、贡献流程和社区运营。
15. [申报与演示](04_OPEN_SOURCE/GRANT_AND_DEMO.md)：申报表映射、演示脚本和资助周期成果。
16. [演示影片制作包](04_OPEN_SOURCE/DEMO_FILM/README.md)：可直接录制、剪辑和验收的导演脚本与镜头规范。
17. [申报冲刺](04_OPEN_SOURCE/APPLICATION_FAST_TRACK.md)：第一批截止前的可信 alpha 与材料流程。
18. [团队与资源](05_GOVERNANCE/TEAM_AND_RESOURCES.md)：三人分工、评审责任和两档预算。
19. [决策与风险](05_GOVERNANCE/DECISIONS_AND_RISKS.md)：已定决策、风险和变更规则。
20. [完成定义](05_GOVERNANCE/DEFINITION_OF_DONE.md)：各阶段何时才算真正完成。
21. [追踪矩阵](05_GOVERNANCE/TRACEABILITY_MATRIX.md)：需求、代码、测试、文档和申报成果的对应关系。

## 实施原则

1. **先形成一条真实闭环。** 首先让一个受支持模型完成“视频 + 台词 + 参考音频 → 配音音频 + 合成视频”，再扩展模型数量。
2. **模型是可替换后端，能力是稳定产品接口。** UI 和核心流水线依赖 `ModelCapabilities`，不依赖某篇论文的目录结构。
3. **成熟度公开。** 模型分为 Stable、Experimental、Planned；只有通过可复现推理、许可审核和端到端测试的模型才能标为 Stable。
4. **本地优先。** 默认不上传用户视频、声音和台词；所有素材和模型在本机运行。
5. **不伪造兼容性。** 未在真实硬件、真实模型、真实素材上验证的能力不得写入“已支持”。
6. **研究成果可追溯。** 每个适配器保留原论文引用、许可证、权重来源、提交版本和修改说明。
7. **每个阶段均可发布。** 每一阶段结束时必须得到可运行、可测试、可回滚的版本，而不是一批无法联调的代码。

## 规划状态

本版规划固定了产品方向、`v0.1.0` 范围、技术架构和实施顺序。后续正式实现开始前，只需要完成 `05_GOVERNANCE/DECISIONS_AND_RISKS.md` 中列出的“启动核验”，不再重新讨论总体方向。
