# Application Fast Track

## 时间约束

第一批申报截止时间为 2026 年 7 月 31 日。完整 `v0.1.0` 不应为了申报在六天内仓促伪造。申报前目标是形成一个可信、可审查的 `v0.0.1-alpha`：主仓库存在，定位与架构清楚，有最小可运行工程证据，既有模型成果有明确关系，资助周期交付可验收。

## 截止前最低证据

### 必须具备

- `GalaxyCong/OpenDub` 公开主仓库；
- Apache-2.0、NOTICE、CITATION.cff、CONTRIBUTING；
- 中英文 README；
- 产品定位、架构图、能力地图和 Roadmap；
- 项目 Schema 初版；
- `opendub doctor` 或最小 TestAdapter 流水线中至少一项可运行；
- CI 至少运行格式、类型和单元测试；
- 一段已有研究结果演示，明确标为“技术基础”，不冒充 OpenDub 已完成输出；
- 申请表完整初稿；
- 一页技术文档或公开文档入口；
- 当前版本准确写为 `v0.0.1-alpha`。

### 不应为了截止时间承诺

- 已整合所有模型；
- 已完成多语言、长视频或国产 GPU；
- 已完成未经真实测试的情感强度控制；
- 已发布稳定模型权重；
- 已有大量 OpenDub 用户；
- 已达到生产环境可用。

## 六日推进

### 2026-07-25：规划冻结

- 完成本 TODO 体系；
- 确认 OpenDub 名称、Apache-2.0、主仓库和首版边界；
- 负责人确认申报主体、团队成员和公开联系方式；
- 核对申请表是否有在线表单额外字段。

完成证据：本目录、决策记录、申报字段清单。

### 2026-07-26：仓库与上游审计

- 建立 GitHub 主仓库；
- 完成 Task 1–2；
- 固定 EmoDubber、HPMDubbing、StyleDubber 和声码器的 commit；
- 核验代码与权重许可；
- 将现有 Demo 链接分类为技术基础。

完成证据：公开 README、LICENSE、NOTICE、upstream audit。

### 2026-07-27：可信工程骨架

- 完成 Task 3；
- 建立核心包、Web workspace 和 CI；
- 发布最小 `Project` Schema；
- 实现 `opendub doctor` 的 FFmpeg、Python、GPU 基础检查，或实现 DeterministicTestAdapter 的最小生成。

完成证据：安装命令、自动测试、运行日志、alpha 标签。

### 2026-07-28：产品表达与演示证据

- 完成 Studio 高保真静态框架或真实最小 UI；
- 制作架构图、能力图和用户五阶段流程图；
- 整理已有 HPMDubbing、StyleDubber、EmoDubber 的授权演示；
- 录制 45–60 秒 alpha 演示，清楚区分已实现和路线。

完成证据：截图、短视频、公开文档。

### 2026-07-29：申报书初稿

- 按 `GRANT_AND_DEMO.md` 完整填写申报表；
- 重点写团队连续积累、统一工具目标和可验收资助周期；
- 为每项陈述建立证据索引；
- 由项目负责人审阅技术准确性与承诺范围。

完成证据：独立输出 DOCX、evidence index。

### 2026-07-30：审查与修订

- 执行一次模拟评审：创新性、开源价值、可行性、社区性、合规性；
- 删除没有证据的“已有功能”；
- 检查仓库匿名访问、链接、许可证和演示播放；
- 将 DOCX 转为 PDF 做视觉检查；
- 准备报名上传包。

完成证据：审查记录、最终候选 PDF、上传包清单。

### 2026-07-31：提交与归档

- 负责人核对姓名、电话、邮箱和仓库；
- 在截止时间前至少 4 小时提交；
- 保存提交回执、最终 DOCX/PDF、视频、技术文档和仓库 commit；
- 在仓库建立 Seed Fund milestone，开始按 Task 4–28 推进。

完成证据：回执、归档哈希、milestone。

## Alpha 仓库首屏

申报时 README 必须清晰区分三层：

- **Available now**：真实完成的仓库骨架、Schema、诊断或 TestAdapter。
- **Research foundations**：HPMDubbing、StyleDubber、EmoDubber 等既有成果。
- **Seed-fund roadmap**：真实模型适配、Web Studio、统一评测和成片导出。

这样既展示团队实力，也不会把既有论文结果伪装成 OpenDub 当前完成度。

## 申报包

```text
种子计划+OpenDub/
├── 青年开源种子计划申报表-OpenDub.docx
├── OpenDub-技术说明.pdf
├── OpenDub-alpha-demo.mp4
├── OpenDub-项目仓库与证据链接.pdf
└── README.txt
```

若报名系统只允许表单和链接，保留相同归档目录作为团队内部提交快照。

## 快速评审清单

- 评审能否在 30 秒内说出 OpenDub 与普通 TTS 的区别？
- 是否只有一个项目名称和一个主仓库？
- 既有模型是否被写成技术基础和产品能力，而非多个并列项目？
- 当前完成、资助期目标和长期路线是否清楚区分？
- 资助金额是否足以覆盖承诺？
- 是否有真实代码、测试、文档或演示证据？
- 是否说明声音授权、数据版权和模型许可？
- 是否有一个可持续维护者和明确分工？

任一答案为“否”，提交前必须修订对应材料。
