# OpenDub 申报证据索引

> 状态说明：**已验证** 表示当前仓库有可执行代码和自动化验证；**条件升级** 表示目标明确但只有满足证据门槛后才能写入“已有功能”；**待人工补充** 表示需要负责人、发布平台或授权方提供事实。申报时不要以“计划”替代“已实现”。

| 申报陈述 | 状态 | 仓库证据 | 验证方式 | 视频呈现 |
| --- | --- | --- | --- | --- |
| 三个完整视频配音方法可被交互式解释与检视 | 已验证 | `content/methods/*/method.json`、`apps/web/src/features/methods/` | manifest 校验、前端组件测试、生产构建 | Atlas 与任一 Method Canvas |
| 用户可从 Atlas 把一个完整方法带入本地项目 | 已验证 | `apps/web/src/features/methods/MethodAtlasPage.tsx`、`MethodCanvasPage.tsx`、`StudioApp.tsx` | 三个方法的路由/选择测试 | 选择 `Prepare project` |
| 方法选择记录包含固定证据版本并由 API 校验 | 已验证 | `src/opendub/domain/project.py`、`src/opendub/api/app.py` | `tests/unit/domain/test_project.py`、`tests/integration/api/test_projects.py` | Studio 显示方法与 `CONCEPT` 状态 |
| 本地项目以版本化 `project.json` 为真相源 | 已验证 | `src/opendub/domain/project.py`、`src/opendub/storage/project_store.py` | `tests/unit/storage/test_project_store.py` | Studio 项目 revision |
| 视频、文本和参考语音的准备条件可以记录并校验 | 已验证 | `src/opendub/domain/assets.py`、`project.py`、`preparation_service.py` | `tests/integration/application/test_preparation_service.py` | 授权确认与选中片段 |
| 可导出版本化 `opendub.project-preparation/v1` 清单 | 已验证 | `src/opendub/application/preparation_service.py`、`api/app.py`、`StudioShell.tsx` | `tests/integration/api/test_preparation_export.py`、前端组件测试 | 点击 Export preparation record |
| 参考声音必须关联明确授权 | 已验证 | `src/opendub/domain/project.py`、`src/opendub/api/app.py` | `tests/integration/api/test_project_resources.py` | 导入音频 -> 权属声明 -> 参考声音 |
| 素材以 SHA-256 内容寻址保存 | 已验证 | `src/opendub/storage/artifact_store.py` | `tests/unit/storage/test_artifact_store.py` | 仅展示项目状态，不展示个人路径 |
| 三个方法的来源、commit、许可、权重与运行状态受审计 | 已验证 | `model-registry/upstreams.yaml`、`licenses/UPSTREAM_AUDIT.md`、`docs/atlas/` | `tests/unit/model_registry/test_upstream_audit.py`、Evidence Room | Evidence Room |
| HPMDubbing / StyleDubber / EmoDubber 已作为可用 Live 后端 | 条件升级 | 审计文档说明尚未完成权重与真实推理验证 | 需完整准入记录 | 不得作为已完成能力录制 |
| 真实情感强度控制和新音频生成可用 | 条件升级 | `TODO/03_EXECUTION/IMPLEMENTATION_PLAN.md` P5 | 真实权重、能力测试、情感评价和运行清单 | 不得将 Concept 控制器表述为生成结果 |
| 公共同输入 A/B/C 比较与“最佳方法”结论 | 条件升级 | `apps/web/src/features/compare/` 仅实现证据门控界面 | 两个及以上合格 Replay Bundle | 只说明比较规则与未解锁状态 |
| 已发布 `v0.1.0` | 条件升级 | 当前 `pyproject.toml` 为 `0.0.1a0` | 发布标签、制品、验证报告 | 不得显示为正式版 |
| 正式用户案例、Stars、下载或外部贡献 | 待人工补充 | 无固定仓库事实 | 申报当天核验公开链接和书面许可 | 当前填写“暂无”或核验后填写 |

## 可录制的申报 Alpha 路径

1. 从 `/explore` 解释 `Video + Target Text + Authorized Reference Speech -> Target Speech -> Dubbed Video`；
2. 在 `/methods` 比较三个完整方法的研究侧重点，而不声称哪一个“全局最好”；
3. 打开一个 Method Canvas，点击其组件并展示 `Concept` 标记和证据入口；
4. 从该方法点击 `Prepare project`，展示 Studio 中已保存的方法、输入要求和不可用的 Live 状态；
5. 使用自制或明确授权素材创建一个片段，登记输入确认并导出准备记录；
6. 打开 `/evidence`，说明为什么没有通过准入的 checkpoint 不会被伪装为可运行模型。

这条路径完整、可运行、可复现，但不模拟真实模型效果。正式录制前须由非项目成员逐句核对本表，确认没有把 `Concept`、准备记录或测试适配器输出说成真实配音生成结果。
