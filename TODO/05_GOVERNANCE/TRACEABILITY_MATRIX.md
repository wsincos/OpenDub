# Traceability Matrix

## 产品承诺到工程证据

| 产品承诺 | 领域/模块 | 主要任务 | 测试证据 | 用户证据 |
|---|---|---|---|---|
| Scene-aware | Media、Vision、HPM Adapter | 7、8、29 | media integration、HPM real smoke | 视频条件与时间线 Demo |
| Character-consistent | VoiceReference、Adapter、speaker metric | 4、12、16 | voice contract、speaker direction test | 参考声音绑定与音色指标 |
| Emotion-directed | EmotionSpec、EmoDubber Adapter、emotion metric | 4、12、16、22 | parameter effect、emotion metric | neutral/happy A/B Demo |
| Timeline-ready | TimeRange、Timeline、Render | 4、8、21、23 | sample-exact render、seek E2E | 波形、偏差和 MP4 导出 |
| Reproducible | Run manifest、Registry、WeightManager | 2、5、9、14 | schema、hash、cache tests | run.json 与报告 |
| Local-first | Config、API、Safety | 3、17、26 | bind/privacy/security tests | Docker/原生本地运行 |

## `v0.1.0` 能力到文件

| 能力 | 规划文件 | 未来代码位置 |
|---|---|---|
| 项目管理 | USER_WORKFLOWS、DOMAIN_CONTRACTS | `domain/`、`storage/`、`application/project_service.py` |
| 视频导入 | SYSTEM_ARCHITECTURE | `media/probe.py`、`media/proxy.py` |
| 台词时间线 | PRODUCT_EXPERIENCE | `media/timeline.py`、`features/timeline/` |
| 声音授权 | SAFETY_LICENSING | `domain/assets.py`、`features/voices/` |
| 情感控制 | CAPABILITY_AND_MODEL_MAP | `adapters/emodubber/`、`features/emotion/` |
| 模型接入 | DOMAIN_CONTRACTS | `models/`、`adapters/` |
| 声码器 | CAPABILITY_AND_MODEL_MAP | `adapters/hpm_vocoder/` |
| 任务队列 | SYSTEM_ARCHITECTURE | `jobs/`、`pipeline/` |
| 候选比较 | PRODUCT_EXPERIENCE | `features/candidates/` |
| 统一评测 | SCOPE_AND_SUCCESS | `evaluation/`、`features/evaluation/` |
| 成片导出 | USER_WORKFLOWS | `media/render.py`、`features/export/` |
| CLI | SCOPE_AND_SUCCESS | `cli/` |
| REST/SSE | SYSTEM_ARCHITECTURE | `api/` |
| Web Studio | PRODUCT_EXPERIENCE | `apps/web/` |
| 容器与发布 | RELEASE_OPERATIONS | `deploy/`、`.github/workflows/` |

## 模型到功能与状态

| 模型/仓库 | 功能 | 首版状态 | 升级证据 |
|---|---|---|---|
| EmoDubber | Emotion Director、Character Voice | 目标 Stable | 情感作用测试、真实 smoke、许可 |
| HPMDubbing_Vocoder | Acoustic Renderer | 目标 Stable/Experimental | mel 契约、权重哈希、真实音频 |
| HPMDubbing | Visual Sync Engine | `v0.2.0` Experimental | 自动视频预处理、真实 smoke |
| StyleDubber | Style Director | `v0.2.0` Experimental | 风格作用测试、真实 smoke |
| HD-Dub/HDCode | 高级同步 | Planned | 源码/权重/许可/契约 |
| CoSyncDiT | 同步扩散 | Planned | 正式代码与权重 |
| LLM-Flow-Dubber | 上下文/指令控制 | Planned | 可运行模型资产 |

## 申报栏目到证据

| 申报栏目 | 规划来源 | 实际提交证据 |
|---|---|---|
| 项目背景 | PROJECT_CHARTER | README、既有论文/仓库 |
| 主要功能 | SCOPE_AND_SUCCESS | `v0.1.0` Release、Demo |
| 技术架构 | SYSTEM_ARCHITECTURE | 架构文档、代码目录 |
| 创新点 | PROJECT_CHARTER、CAPABILITY MAP | Adapter SDK、统一 Schema、Quality Lab |
| 社区贡献 | DOCUMENTATION_COMMUNITY | 既有仓库数据、Issue、Release |
| 兼容适配 | QUALITY_PLAN | 支持矩阵与验证报告 |
| 技术文档 | DOCUMENTATION_COMMUNITY | 文档站 |
| 演示视频 | GRANT_AND_DEMO、DEMO_FILM | 2:40 正式片、60 秒预告、30 秒循环和证据索引 |
| 阶段目标 | IMPLEMENTATION_PLAN | M1/M2/M3 milestone |
| 商业化计划 | GRANT_AND_DEMO | 开源核心与服务边界说明 |
| 后续路线 | CAPABILITY MAP | `v0.2.0`/`v0.3.0` Roadmap |
| 希望支持 | GRANT_AND_DEMO | 算力、合规、场景、社区需求 |

## 版本门槛到任务

| 里程碑 | 必需任务 |
|---|---|
| M1 | 1–11、17–18 的最小 API/CLI |
| M2 | 12–16、14、真实 GPU 验证 |
| M3 | 19–28 |
| `v0.2.0` | 29–30 |
| 研究准入 | 31 |
| 正式演示影片 | 32 |

## 变更检查

任何需求变更提交前回答：

1. 它改变了哪项产品承诺？
2. 它改变了哪个 Schema、接口或状态？
3. 哪个任务和测试需要更新？
4. 用户文档和 UI 是否变化？
5. 模型卡、许可证或权重清单是否变化？
6. 申报材料中的陈述是否仍然准确？

六项中任一有变化，都必须更新本矩阵对应行。
