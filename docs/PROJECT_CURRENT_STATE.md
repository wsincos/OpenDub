# OpenDub 项目当前状态说明

**更新时间：** 2026-07-26<br>
**主仓库：** <https://github.com/wsincos/OpenDub><br>
**当前开发版本：** `v0.0.1-alpha.0`

## 1. 一句话结论

OpenDub 当前已完成申报版的 **P0-P3 交付闭环**：它可以清楚解释视频配音生成任务、交互式展示并选择三套完整研究方法、将选择和授权输入保存为本地项目，并导出可复现的准备记录。申报演示视频、双语字幕、校验和和交付清单已随仓库提供。

当前版本没有把任何未通过证据门槛的模型伪装成可用的 Live 推理能力，也没有伪造多方法音频比较结果。

对外统一名称为：

> **OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台**<br>
> **OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing**

产品特征描述为：**Interactive Method Atlas, Visual Comparison, and Complete-Method Workbench**。

## 2. OpenDub 解决什么问题

视频配音不是单纯的文本转语音。目标视频提供口型、表情、场景和时间节奏；目标文本给出要说的内容；经授权的参考语音给出可使用的声音身份或风格。OpenDub 将任务表达为：

```text
Video + Target Text + Authorized Reference Speech
                    -> one complete dubbing method
                    -> Target Speech -> Dubbed Video
```

平台不从不同论文中抽取网络模块再拼成一个“新模型”。它保留每项工作作为独立、完整的方法，并提供统一的解释、选择、准备、证据和后续准入路径。

## 3. 当前的核心体验

### 3.1 Task Explorer：先讲清楚任务

入口：`/explore`

- 交互解释 Video、Target Text、Authorized Reference Speech 的不同作用；
- 明确区分研究输出 `Target Speech` 与产品输出 `Dubbed Video`；
- 用同步时间线说明视觉、文本、韵律和输出的关系；
- 所有示意波形、频谱和画面均标记为 `Concept`，不会被表述为新生成音频。

### 3.2 Method Atlas：展示团队已有的三套完整方法

入口：`/methods`

| 方法 | 平台中说明的研究重点 | 当前公开状态 |
| --- | --- | --- |
| HPMDubbing | Lip、Face、Scene 分层视觉线索如何影响时长、音高、能量和整体情感 | `Concept` |
| StyleDubber | Frame、Phoneme、Utterance 多尺度表示如何共同学习说话风格 | `Concept` |
| EmoDubber | 同步、清晰度、身份与情感引导如何共同约束视频配音 | `Concept` |

每个方法页都可点击查看真实论文信息流中的组件、边、信号、论文、源码和证据。三个页面还各有一个专属的机制互动视图：分层韵律、多尺度对齐或情感引导。

Atlas 首屏另提供按首要需求的可解释导览：视觉韵律与场景节奏对应 HPMDubbing，发音清晰度与角色风格对应 StyleDubber，显式情感方向对应 EmoDubber。它只建议“优先理解 / 准备”的完整方法，不宣称全局最优或实时生成。

### 3.3 从方法选择到本地项目准备

用户可从 Atlas 或任何 Method Canvas 点击 **Prepare project**。平台会将下列记录写入项目：

- 方法 ID、声明用途、输入要求和可选控制项；
- 固定的 Method Manifest / evidence revision；
- 方法的内容状态和运行状态。

服务端读取对应 manifest 后校验记录，因此客户端不能把旧版本证据或错误方法伪装成一次有效选择。

Studio 进一步支持：

1. 创建本地项目、导入本地素材和维护整数微秒时间线；
2. 对参考语音登记素材来源和使用同意；
3. 对当前视频记录授权声明，对当前目标文本记录指纹确认；
4. 要求每个片段引用同一所选完整方法及已同意的参考语音；
5. 导出 `opendub.project-preparation/v1` 准备清单。

准备导出会重新校验视频 SHA-256、文本指纹、参考语音同意记录、时间线和方法一致性。该清单是后续方法作者或合格 Adapter 的可复现输入交接，不是一次生成请求。

### 3.4 Evidence Room 与比较边界

入口：`/evidence` 和 `/compare`

Evidence Room 为每项方法显示论文、固定源码提交、代码许可、权重状态和运行状态。当前三个方法均处于可交互的 `Concept`，尚未作为 OpenDub 的 Live 后端发布。

Comparison Lab 已定义“相同视频、文本、参考语音、时间策略和权利记录”的公平比较规则，但没有合格的同输入 Replay Bundle 时不会显示假音频、假指标或全局排名。

## 4. 申请版系统架构

![OpenDub 平台架构](architecture/opendub-platform-architecture.svg)

架构源文件为 [可编辑 draw.io 文件](architecture/opendub-platform-architecture.drawio)。图中描述的是平台的数据、选择和证据流，刻意不画成一个把三篇论文混合起来的神经网络。

## 5. 已完成与未宣称的边界

| 能力 | 当前状态 | 可如实表述 |
| --- | --- | --- |
| 任务解释、方法 Canvas、组件交互 | 已完成 / `Concept` | 可以交互理解并检查三个完整方法 |
| 选择记录、授权项目与准备导出 | 已完成 | 可以选择一个方法，保存授权输入并导出准备清单 |
| 同输入公开结果回放与比较 | 条件升级 | 已定义规则；需合格 Replay Bundle 后开放 |
| 真实模型推理与新音频生成 | 不可用 | 需一个完整方法通过代码、权重、许可、哈希、隔离环境和真实 smoke test 准入 |
| 情感控制的真实输出效果 | 不可用 | 目前只展示机制和准备字段，不展示新的控制效果音频 |

## 6. 申报与录制材料在哪里

- [申报摘要](grant/project-summary.md)：可直接用于填写申报表的事实底稿；
- [证据索引](grant/evidence-index.md)：每项功能声明对应的代码、测试和视频画面；
- [演示视频交付](grant/video/README.md)：110 秒 MP4、中英字幕、校验和、来源和事实边界；
- [演示脚本](grant/demo-script.md)：录制路径、旁白和事实边界；
- [平台架构图](architecture/README.md)：可编辑 draw.io 源与 SVG；
- [完整规划](../TODO/README.md)：后续开发、质量、发行、视频和条件升级计划。

## 7. 当前验证记录

本次申报材料冻结前已完成以下检查：

| 检查项 | 结果 |
| --- | --- |
| Python 格式、静态检查、类型检查与测试 | `108 passed`；仅保留一个上游 `Starlette TestClient` 弃用警告 |
| Web 类型检查、组件测试与生产构建 | 已纳入 `make check` / CI 强制门禁；TypeScript 通过，`11` 个文件、`22` 项组件测试通过，Vite 生产构建通过 |
| 内容与模型注册表 | `3 method manifests validated`；Registry 校验通过 |
| 文档与差异检查 | 本地 Markdown 链接与 `git diff --check` 通过 |
| 浏览器 QA | 在 `1440x900` 检查 Task Explorer、Method Atlas、Studio 已选方法界面；在 `390x844` 检查 Task Explorer 与 Method Atlas；无重叠或截断 |
| 本地端口回归 | Studio 已在替代 Vite 端口 `5180` 对本地 API 完成 CORS 访问验证 |
| 申报视频交付 | `110.043` 秒、`1920x1080`、30 FPS；MP4 内嵌中英字幕轨，独立 SRT 与 SHA-256 见视频交付目录 |
| 申报 Word 表 | OpenXML 校验通过；LibreOffice 渲染为两页 A4 并完成视觉检查 |

## 8. 录制时最重要的三句话

1. “OpenDub 让视频配音方法变得可理解、可选择、可准备、可核查。”
2. “HPMDubbing、StyleDubber 和 EmoDubber 是三套完整方法，不是被拼接成的新模型。”
3. “Concept 解释机制；Replay 与 Live 只有在证据通过后才开放。”

这些边界不是功能缺陷，而是开源平台对可复现性、素材权利和用户信任的基本承诺。
