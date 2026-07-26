# OpenDub 青年开源种子计划严格审核（第 2 轮）

**审核日期：** 2026-07-26
**审核角色：** 独立、严格的青年开源项目评审
**审核对象：** `OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台`
**对比基线：** [第 1 轮审核](round-01-strict-audit.md) 的 `8.0 / 10` 与两项 P0：远端未发布、正式视频未交付。

## 最终结论

**本轮总分：9.2 / 10，达到 `>= 9 / 10` 的种子计划申报门槛。**

第 1 轮的两项 P0 已完成闭环：当前申报版已在远端 tag `v0.0.1-alpha.0` 中发布，且已经提供可校验的 110 秒申报视频、独立双语字幕、内嵌字幕轨、旁白文本和事实边界清单。平台仍诚实地保持 `Concept` 状态，没有把没有权重、许可、哈希和真实 smoke test 的方法说成 Live，也没有用虚构 Replay 来增加演示效果。

这不是“模型已全面可运行”的评分。9 分来自一个可信、可复核、交互成熟的**开源种子项目申请版本**：它把团队已有的三套完整视频配音研究方法做成可理解、可选择、可准备、可核查的平台，并将真实运行作为有明确证据门槛的下一阶段。

## 评分

| 维度 | 第 1 轮 | 第 2 轮 | 严格审核结论 |
| --- | ---: | ---: | --- |
| 申请叙事 | 8.3 | **9.3** | 名称、任务输入输出、三个完整方法、证据边界和阶段规划一致；按首要需求的选择导览已补齐。 |
| 差异化 / 创新 | 8.8 | **9.4** | “完整方法而非模块拼装”“可交互机制解释”“证据与授权默认进入工作流”形成了清楚、可信的组合价值。 |
| 交互与专业感 | 8.9 | **9.2** | Task Explorer、Method Atlas、Method Canvas、Evidence Room 的研究工具视觉语言成熟；选择器具有中英双语关键提示，视频画面具备专业演示完成度。 |
| 用户路径可用性 | 7.4 | **9.0** | `理解 -> 按需求导览 -> 选择完整方法 -> 本地授权准备 -> 可复现准备导出 -> 证据核查` 已构成可演示路径，且没有谎称已生成。 |
| 技术真实性 / 证据 | 8.2 | **9.5** | 远端 tag、干净 clone、自动化质量门、方法 Manifest、上游审计和视频事实边界相互一致。 |
| 申报交付物 / 演示力度 | 5.8 | **9.1** | MP4/SRT/SHA-256/交付清单/Word 已闭环；视频克制但清晰，尚可通过少量后期优化提升冲击力。 |
| **总分** | **8.0** | **9.2** | **达到申报门槛。** |

## 本轮独立复核证据

### 1. 远端 tag、主分支与干净 clone 一致

已使用 Git 远端而非本地工作树进行核验：

```text
origin/main                         ff39ff3c9c66c0bab0cc7c51a61db07ed6db0d69
refs/tags/v0.0.1-alpha.0^{}        ff39ff3c9c66c0bab0cc7c51a61db07ed6db0d69
```

- `v0.0.1-alpha.0` 是带注释 tag，说明为 `OpenDub application alpha: interactive atlas, preparation workflow, evidence boundary, and audited video delivery`。
- 以远端 `https://github.com/wsincos/OpenDub.git`、`--branch v0.0.1-alpha.0 --depth 1` 创建全新 clone；clone 的 `HEAD`、精确 tag 均为 `ff39ff3`，`git status --short` 为空。
- clone 中实际存在本申请依赖的 [准备导出服务](../src/opendub/application/preparation_service.py)、[架构图](../docs/architecture/opendub-platform-architecture.svg)、[按需求选择组件](../apps/web/src/features/methods/MethodAtlasPage.tsx) 和 [视频交付清单](../docs/grant/video/delivery-manifest.json)。
- clone 中 MP4 的 SHA-256 与本地、交付清单完全一致：

```text
57df9c798f0f50cbc01132e7389722e18fdcdc9e090cd5486b27a6558bdbad26
```

**结论：** 第 1 轮“申请链接与本地展示不一致”的 P0 已关闭。

### 2. 视频交付真实存在、可校验、且事实边界可复核

已逐项检查 [视频交付目录](../docs/grant/video/README.md)：

| 项目 | 独立核验结果 |
| --- | --- |
| MP4 | `OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4` 存在，`3,785,764` bytes。 |
| 哈希 | 在 `docs/grant/video/` 中执行 `sha256sum -c`，结果为 `OK`。 |
| 时长与画幅 | FFprobe：`110.043` 秒、`1920x1080`、30 FPS、3300 视频帧。 |
| 音频 | 单声道 AAC、24 kHz、110 秒；音量检测为 `mean -24.8 dB`、`max -3.0 dB`，不是空音轨。 |
| 字幕 | MP4 有 `mov_text` 字幕流，语言标识 `zho`；独立 [中英 SRT](../docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0_CN_EN.srt) 覆盖 0–110 秒。 |
| 旁白与边界 | [旁白文本](../docs/grant/video/narration.zh-CN.txt) 与 [交付清单](../docs/grant/video/delivery-manifest.json) 均明确旁白是说明产品流程的合成旁白，**不是** OpenDub 或上游方法输出。 |

抽帧检查覆盖 1、10、15、25、30、40、55、65、75、85、95、105、109 秒：任务解释、按需求选择、三种方法、EmoDubber Canvas、Studio、Evidence Room 与 Comparison Lab 均实际出现在成片中。画面显示 `CONCEPT`、`GATE CLOSED`、`0 / 3 verified replay bundles`、`Zero invented outputs` 等真实边界；没有假音频播放器、假指标或“已 Live”标签。

**结论：** 第 1 轮“只有脚本，没有视频成片”的 P0 已关闭。视频并不靠虚构音频制造效果，这一点与本项目的证据定位一致。

### 3. 申请 Word 表在本地仍是可提交的两页版本

对 [申报版 Word 表](../original/OpenDub_青年开源种子计划申报表_申报版_v0.0.1.docx) 的 OpenXML 结构和 LibreOffice 渲染进行了复核：

- 一个主表，项目名称、仓库、许可证、当前版本与发布 tag 一致；
- “主要功能”已写入按需求选择的准确边界，不使用“全局最优”措辞；
- “项目演示视频”明确列出 110 秒 MP4、字幕、SHA-256 和事实边界，并明确旁白不是模型输出；
- PDF 渲染为 **2 页 A4**，无第三页溢出、截断或表格重叠。

表中仍把视频作为“随申报材料附送”的仓库相对路径。这符合模板允许将视频和文档一并上传的注释；在实际提交包中应保留该 MP4 文件及其清单，不要只上传 Word。

### 4. 可解释选择引导已经成为真实交互，而非文案承诺

[Method Atlas](../apps/web/src/features/methods/MethodAtlasPage.tsx) 现提供：

- `Visual prosody and scene rhythm / 视觉韵律与场景节奏` -> HPMDubbing；
- `Pronunciation and character style / 发音清晰度与角色风格` -> StyleDubber；
- `Explicit emotion direction / 显式情感方向` -> EmoDubber。

选择结果明确写为 `Recommended for inspection and preparation / 可解释导览`，并保留两条动作：检查方法与证据、准备这一完整方法。边界文字明确说明：这不是 Live runtime 或全局最优声明。其对应组件测试验证 EmoDubber 的路由和边界文字。

Chromium 桌面与 `390x844` 移动端检查显示：三项需求均可见、选中状态清晰、中文解释不被裁切；视觉层级足以在申报视频中让中文评审快速理解选择逻辑。

### 5. CI/Makefile 已覆盖此前遗漏的 Web 门禁

[Makefile](../Makefile) 的 `check` 现在包含：

```text
format -> lint -> type -> pytest -> web TypeScript check
-> web Vitest -> web production build -> docs link check
```

[GitHub Actions](../.github/workflows/ci.yml) 在 `main` push 和 Pull Request 上运行 `make check`，并额外校验模型 Registry。当前本地按该门禁实测结果为：

- Ruff 格式与静态检查通过；
- Mypy：`72` 个源文件无问题；
- Python：`108 passed`，仅保留已知 Starlette TestClient 弃用警告；
- Web：`11` 个测试文件、`22 passed`；
- Vite 生产构建通过；
- 文档链接、3 份 Method Manifest、模型 Registry 均通过。

本审核无法通过 GitHub REST API 读取远端 Actions 的运行页面（匿名 API 返回 403），但这**不阻碍 9 分结论**：远端 clone 已验证，且本地针对相同 tag 内容成功执行了 CI 相同质量命令。提交前可在 GitHub 网页补看该 tag 所在提交的绿色 Actions 状态。

### 6. Concept / Replay / Live 的真实边界仍被保持

本轮没有发现为提高视频效果而破坏可信边界的迹象：

- 三个 `content/methods/*/method.json` 都仍为 `runtime_status: unavailable`；
- [Evidence Room](../apps/web/src/features/evidence/EvidenceRoomPage.tsx) 显示权重条款、哈希、隔离 smoke test 与 public replay 仍未满足；
- [Comparison Lab](../apps/web/src/features/compare/ComparisonLabPage.tsx) 在无合格 case 时禁止 Replay 与排名；
- [视频清单](../docs/grant/video/delivery-manifest.json)、[项目当前状态](../docs/PROJECT_CURRENT_STATE.md)、[申报 Word](../original/OpenDub_青年开源种子计划申报表_申报版_v0.0.1.docx) 对 `Concept`、`Replay`、`Live` 的含义一致。

没有 Live checkpoint 不是扣分点。对于种子计划，这恰好说明资金、算力和合规支持将被用于一个可审计的后续准入路径，而不是被用于包装未经验证的结果。

## 仍然建议处理的问题

### P1-1：提交包中增加一个稳定的公开视频链接或 Release 附件说明

当前 MP4 已随仓库版本提供，Word 也声明“随申报材料附送”，因此**不是 P0**。不过如果申报系统允许外链，建议在提交时同时提供该 tag 的 GitHub Release 地址或组织指定的稳定视频链接，并把 Word 中的视频说明改成“随附 MP4 + 可访问链接”。这样能避免评审只打开仓库但未下载二进制文件时遗漏视频。

**验收：** 申报压缩包含 MP4、SRT、SHA-256、`delivery-manifest.json`；若有在线链接，链接的文件哈希与清单一致。

### P1-2：为最终成片加入一个更聚焦的“结果摘要”转场

视频画面和叙事已经专业、清晰，但整体仍偏研究工作台录屏。在 110 秒内可加入约 2 秒的静态转场，收束为：

```text
Understand -> Choose -> Prepare -> Verify
OpenDub v0.0.1-alpha.0 | Concept Atlas | No invented outputs
```

这会进一步强化记忆点和视觉冲击，但不得加入不存在的音频波形、性能数字、Live 标签或模型效果承诺。

**验收：** 增强版仍保持 95–110 秒、同一 hash/版本清单更新、字幕和旁白同步复核。

### P2-1：少量术语可继续面向非技术评审降噪

Word 的 `Method Manifest`、`preparation manifest`、`adapter`、`smoke test` 均准确，但可在首次出现时补一句短中文释义。此项不影响本轮可提交性，属于降低评审理解成本的文案优化。

### P2-2：GitHub Actions 的运行状态应在提交当天人工复核

工作流定义和本地同命令结果均通过；匿名 GitHub API 的 403 使本审核无法读取远端 Actions 状态。提交者应在 tag/commit 的 Actions 页面确认最后一次 `quality` job 绿色，并在申请材料冻结记录中保存 run URL 或截图。

## 最终提交建议

当前版本已可作为项目申请提交。提交前只需做发布操作层面的最终核对：

1. Word、MP4、SRT、SHA-256、交付清单和源码均来自 `v0.0.1-alpha.0` / `ff39ff3`；
2. 申请系统实际上传视频时，使用仓库内已校验的 MP4，而不是重新导出一个未更新 hash 的副本；
3. GitHub Actions 页面显示该发布提交的 `quality` job 绿色；
4. 申请口径继续使用“可理解、可选择、可准备、可核查”，不把 `Concept` 说成真实生成。

在上述提交动作保持一致的前提下，**OpenDub 达到 9.2 / 10，足以进行青年开源种子计划项目申请。**
