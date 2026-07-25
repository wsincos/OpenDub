# OpenDub 申报证据索引

> 状态说明：`已验证` 表示当前仓库有可执行代码和自动化验证；`规划中` 表示目标明确但不可写入“已有功能”；`待人工补充` 表示需要负责人或发布平台提供事实。

| 申报陈述 | 状态 | 仓库证据 | 验证方式 | 视频呈现 |
| --- | --- | --- | --- | --- |
| 本地项目以版本化 `project.json` 为真相源 | 已验证 | `src/opendub/domain/project.py`、`src/opendub/storage/project_store.py` | `tests/unit/storage/test_project_store.py` | 00:40 后 Studio 项目状态 |
| 时间线使用整数微秒，片段绑定目标时间窗 | 已验证 | `src/opendub/domain/time.py`、`src/opendub/domain/segments.py` | `tests/unit/domain/test_time.py` | Studio 时间线、片段详情 |
| 媒体命令不经过 shell，支持探测/字幕/渲染基础 | 已验证 | `src/opendub/media/` | `tests/integration/media/` | 仅展示已完成的本地导入；最终渲染镜头须待 M2 |
| 参考声音必须关联明确授权 | 已验证 | `src/opendub/domain/project.py`、`src/opendub/api/app.py` | `tests/integration/api/test_project_resources.py` | 导入音频 -> 权属声明 -> 参考声音 |
| 素材以 SHA-256 内容寻址保存 | 已验证 | `src/opendub/storage/artifact_store.py` | `tests/unit/storage/test_artifact_store.py` | 可展示本地项目素材状态，不展示用户路径 |
| 模型来源、commit、许可和权重状态受审计 | 已验证 | `model-registry/upstreams.yaml`、`licenses/UPSTREAM_AUDIT.md` | `tests/unit/model_registry/test_upstream_audit.py` | 02:07 后仅显示真实 `planned` 状态 |
| EmoDubber/HPMDubbing 已作为 OpenDub 可用后端 | 规划中 | `docs/audits/` 说明尚未完成权重/真实推理验证 | 不可通过 | 不得作为已完成镜头或功能宣称 |
| 真实情感强度控制可用 | 规划中 | `TODO/03_EXECUTION/IMPLEMENTATION_PLAN.md` Task 12 | 需真实权重、能力测试和情感指标 | 不得录制“生成成功”或 A/B 结论 |
| 测试适配器能验证候选、运行清单和追溯结构 | 已验证 | `src/opendub/models/testing.py`、`src/opendub/application/generation_service.py` | `tests/integration/application/test_generate_segment.py` | 可用于开发说明，不可伪装为配音效果 |
| Web Studio 可创建项目、导入本地媒体、登记授权和新增片段 | 已验证 | `apps/web/src/app/shell/StudioShell.tsx` | 浏览器 QA：2026-07-25；`make web-check` | 00:40–01:02 可如实录制 |
| 已有正式用户案例 | 待人工补充 | 无 | 需用户书面授权和公开链接 | 当前填写“暂无” |
| 已发布 `v0.1.0` | 规划中 | 当前 `pyproject.toml` 为 `0.0.1a0` | 发布标签、制品、验证报告 | 不得显示为正式版 |
| 社区 Stars、下载、Issue 与外部贡献 | 待人工补充 | 上游 GitHub 主页与 OpenDub 发布页 | 申报当天人工核验 | 仅展示可公开核验数据 |

## 可录制的申报 Alpha 路径

1. 在本机启动 API 与 Studio，创建一个新项目；
2. 导入自制/授权音频；
3. 选择权属来源并登记参考声音；
4. 新增具有文本、时间窗和情感方向的片段；
5. 选择片段，展示时间线、项目 revision 与“模型尚未验证”的明确状态；
6. 切换到 `docs/audits/` 或模型状态页，说明后端的准入原则和后续计划。

这条路径的特点是完整、可运行且不模拟真实模型效果。正式 2 分 40 秒影片中涉及真实生成、候选 A/B、情感结论、评测和成片导出的段落必须等到 M2 证据齐备后再制作。

