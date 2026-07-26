# OpenDub V2 严格申报审核（第 4 轮，最终候选）

**审核日期：** 2026-07-27
**审核角色：** 独立严格审核者（不参与实现）
**审核冻结对象：** commit `71fb1c605078a55b9fc484e75a26a6ad98173ffd`，本地候选 tag `v2.0.0-showcase-rc.1`
**审核范围：** `/vtts`、`/examples`、`/methods`、`/studio`、`/evidence`、V2 申报片、案例/权利记录、可复现交付物和发布门禁。
**结论：** **有条件通过，9.1 / 10，达到本轮“至少 9 / 10”的申报候选门槛。**

本轮没有发现 P0 阻塞项。V2 已经从“静态网页截图集合”变为可核验的任务优先展示：先解释视频配音任务的三类输入、完整方法和两类输出，再展示可点击的观察线索、带边界的历史成果、完整方法图谱和 Evidence Room。尤其重要的是，它没有把任务说明、历史样例或 `Concept` 方法说成 fresh run、Replay、Live 推理或同输入排行榜。

本结论允许以该**冻结候选**继续准备青年开源种子计划材料；在对外宣布正式发布前，仍必须完成本报告的两项 P1 收口事项。

## 本轮结论先行

| 审核问题 | 判断 |
| --- | --- |
| 任务是否讲清楚 | 是。`Silent Video + Target Text + Authorized Reference Speech -> One Complete Method -> Target Speech + Dubbed Video` 在首页、视频、字幕和当前状态说明中一致。 |
| “整合”是否被误导成拼接模型 | 否。平台展示并选择 HPMDubbing、StyleDubber、EmoDubber 三个**完整方法**，明确拒绝混接论文内部模块。 |
| 历史视频是否被虚假包装为新结果 | 否。两类案例都固定标记为 `Archived research example`；影片案例段明确标注 `AUDIBLE: GT`。 |
| 首 20 秒是否为真正的动态演示 | 是。三段由 Playwright 录制的浏览器交互被拼入成片，包含任务流、线索切换和时间线拖动。 |
| 是否仍有此前的白闪或 Studio 错误镜头 | 未发现。最终 MP4 前 20 秒逐帧亮度检查无白帧；影片已移除 Studio 状态镜头和相关能力暗示。 |
| 方法是否被虚假标为可运行 | 否。方法仍为 `Concept` / unavailable；Evidence Room 和影片均保留该边界。 |
| 是否可交付、可校验 | 候选级别可以。MP4、SRT、交付 manifest 和独立 SHA-256 一致，干净检出能校验公开媒体；正式远端发布尚待完成。 |

## 已关闭的上一轮 P0 问题

### 1. 动态流程和声音边界已修复

上一轮的主要问题是成片以静态 PNG 为主。当前构建脚本在 [scripts/build_v2_showcase_film.sh](../scripts/build_v2_showcase_film.sh#L28) 中实际处理三段 `assets/clips/*.webm` 浏览器录像，并在 [69-71 行](../scripts/build_v2_showcase_film.sh#L69) 将它们作为前 20 秒的任务、线索和时间线段落。录制脚本明确执行了 `/vtts?tour=flow`、Face/Lip/Environment 点击以及同步滑块的三个位置更新，见 [capture_v2_web_clips.mjs](../scripts/capture_v2_web_clips.mjs#L17)。

影片没有把非模型声音伪装成生成结果：任务片段的音轨是构建脚本中定义的非语音说明音，并在画面内标为 `CAPTION-LED EXPLANATION / NON-SPEECH AUDIO`；两个案例段只映射 GT 音轨，并在画面内标明 `AUDIBLE: GT`，见 [build_v2_showcase_film.sh](../scripts/build_v2_showcase_film.sh#L39)。字幕也在 20 秒处切换到“已归档研究样例，不是新的 OpenDub 运行”，见 [V2 SRT](../docs/grant/video/v2/OpenDub_VTTS_Showcase_v2.0.0_CN_EN.srt#L17)。

### 2. Playwright 初始白闪已在最终影片中消除

此前发现的片段开头空白过渡已在 [build_v2_showcase_film.sh](../scripts/build_v2_showcase_film.sh#L32) 显式处理：每段浏览器录像从 `-ss 0.5` 开始取材。对最终 MP4 `0.000s` 至 `20.000s` 的 **600 帧**运行 `signalstats`：`YAVG` 最小为 `0.000`、最大为 `55.627 / 255`，没有任一帧达到白帧或白闪水平；在 `7.46/7.50/7.54`、`12.46/12.50/12.54`、`19.96/20.00/20.04` 秒的拼接边界抽帧也没有空白画面。最终联系表和 12 秒转场抽帧均显示为连续、正确的任务页面内容。

### 3. Studio 错误画面及其叙事已从影片移除

[V2 事实边界](../docs/grant/video/v2/fact-check.md#L9) 明确说明当前影片不展示 Studio 网络/API 状态，也不以镜头暗示导出已可用。实际本地 API 的健康检查和项目列表均可工作，但影片不再把该独立工作流作为申报片的可信度支点；这消除了上一轮“画面出现错误、文案仍声称可准备导出”的冲突。

### 4. 完整性清单与候选交付已修复

最终影片为 `84.203` 秒、1920x1080、H.264 30 FPS、AAC 48 kHz 立体声，并含 `mov_text` 中英字幕流。其 SHA-256 为：

```text
0388db63b1a04b7e2480b63b1ba190ec00e8cca5ce94eead35bd31a26ed7a314
```

该值同时出现在 [delivery-manifest.json](../docs/grant/video/v2/delivery-manifest.json#L5) 和 [独立 SHA 文件](../docs/grant/video/v2/OpenDub_VTTS_Showcase_v2.0.0.sha256)，实际执行 `sha256sum -c OpenDub_VTTS_Showcase_v2.0.0.sha256` 通过。重建脚本会在成片和联系表生成后刷新 manifest，再写出相对路径 SHA 文件，见 [build_v2_showcase_film.sh](../scripts/build_v2_showcase_film.sh#L83)。

## 严格复核证据

### 任务表达与交互展示

- `/vtts` 的桌面和移动端均能直接读出三输入、一个完整方法、两输出；输出区固定标为 `Task illustration · no fresh run`。这正是申报项目应首先解释的 VTTS 任务，而不是把用户带进一个没有上下文的研究工作台。
- Face、Lip、Environment 被定位为可解释的观察线索，而不是未公开模型张量；同步时间线展示同源 GT 音频派生的波形、F0、能量和 Mel。历史案例缺 canonical transcript/IPA 的事实被清楚保留，页面 IPA 只作为 `task notation`，见 [当前状态说明](../docs/PROJECT_CURRENT_STATE.md#L35)。
- `/methods` 和 EmoDubber Canvas 把每项贡献放在完整方法路径中。页面导览是“优先理解 / 准备”的建议，不构造未验证的“最佳模型”结论。
- `/examples` 的真人和动画案例各含 GT、HPMDubbing、StyleDubber、EmoDubber 四面板；无分数、无排序、无同输入公平比较暗示。案例 manifest 将 `same_input_across_methods` 明确设为 `false`，例如 [human-0.json](../content/showcases/v2/human-0.json#L22)。

### 事实、权利与证据边界

- [fact-check.md](../docs/grant/video/v2/fact-check.md#L3) 对历史结果、GT 声音、任务说明、`Concept` 状态、浏览器录制和 Studio 移除逐项给出边界。
- 两个 case 都有媒体 SHA-256、方法身份、历史结果来源及 V2 展示授权记录；公开权利文件将权限限定为仓库展示和申请材料，并要求继续使用 `Archived research example` 标识，见 [rights record](../docs/rights/showcase-media-rights-v2.md#L7)。
- 该权利文件没有把项目负责人授权说成第三方版权审计，见其 [verification note](../docs/rights/showcase-media-rights-v2.md#L23)。这比泛化的“已授权”表述更可审查。

### 可复现性与质量门

本轮实测结果如下：

| 检查 | 结果 |
| --- | --- |
| Python 格式、lint、类型和测试 | Ruff 格式/检查通过；mypy 76 个源文件通过；`pytest` 为 `117 passed`，仅 1 个上游 Starlette 弃用 warning。 |
| Web | TypeScript 检查通过；Vitest `13` 个文件、`25` 项测试通过；Vite production build 通过。 |
| 内容与注册表 | `opendub atlas validate --content content` 报 `3 method manifests validated`；上游 registry 校验通过。 |
| 案例派生特征 | `human-0` 和 `animation-1` 的 `build_showcase_features.py --verify-only` 都以退出码 0 通过。 |
| 文档链接 | `.venv/bin/python scripts/check_docs_links.py` 通过。 |
| 视频 | `ffprobe` 与 manifest 的时长、分辨率、帧率、音频及字幕流相符；媒体 SHA-256 通过。 |
| 干净检出 | `/tmp/opendub-v2-clean` 位于 `71fb1c6` 和候选 tag；8 个公开 case MP4 均存在，V2 MP4 SHA-256 校验通过。 |

## 尚需收口的事项

### P1-1：候选尚未推送到远端，不能提前称作“公开正式版本”

**证据：** 当前本地 `HEAD` 是 `71fb1c6`，且 `v2.0.0-showcase-rc.1` 正确指向该提交；但 `origin/main` 仍为旧的 `a3e40f7`，远端只有 V1 的 `v0.0.1-alpha.0` tag。规划文档也正确将候选 tag 视为复审前的临时状态，见 [质量计划](../TODO/07_V2_SHOWCASE/05_V2_QUALITY_RELEASE_AND_AUDIT.md#L29)。

**影响：** 不影响对冻结候选的技术和申报审核分数，但在远端公开前，第三方无法按公开 Git 引用取得本轮代码、案例、影片和审核记录。

**正式发布前的必要动作：** 复审通过后推送冻结 commit，创建并推送新的不可变正式 `v2.0.0-showcase` tag；随后从远端重新 clone，安装锁定依赖，重跑 production build、媒体 SHA 和页面资源访问核验。正式 tag 必须指向本报告审过的内容，不能在同一 tag 上继续改动。

### P1-2：公开包可校验“发布副本”，但不能独立复建原始本地来源链

**证据：** 两个 manifest 的 `source_path` 指向刻意不纳入版本控制的 `reference/example/*.mp4`，例如 [human-0.json](../content/showcases/v2/human-0.json#L28)。干净检出含公开副本、其 SHA、特征和 owner authorization，因此可以核对**公开交付的字节一致性**；但外部 clone 没有原始本地来源媒体，无法独立重跑“原始来源 -> 公开副本”的完整验证。现有权利记录已诚实说明它是项目负责人授权，而非独立版权链审计。

**影响：** 当前“历史、受限范围展示样例”定位没有失实，且不应影响本次种子计划候选；但它不能被宣传为公共 benchmark 或任何第三方都可从原始数据完全复现的结果链。

**正式发布前的必要动作：** 保持 `reference/` 不公开的同时，建立受控的 source-evidence 包或登记表：至少包含权利主体/审批联系通道、每条原始素材的受控 SHA、审批日期、允许范围和撤回处理，不公开身份或源媒体。公开 README 应继续明确：公开可验证的是发布副本、派生特征和展示授权；原始来源核验需经项目维护者受控提供。

### P2-1：一处项目状态文档仍写旧的“86 秒”

[docs/PROJECT_CURRENT_STATE.md](../docs/PROJECT_CURRENT_STATE.md#L113) 第 118 行将 V2 视频写为“86 秒”，实际 MP4、manifest、V2 README 和实现记录均为 `84.203` 秒。该问题不影响文件、字幕或 hash，但正式发布前应改为 `84.203 秒`（或“约 84 秒”），避免申请材料出现可避免的事实漂移。

### P2-2：可选的人声增强，不是事实或发布阻塞项

当前成片是字幕主导版本：任务段使用画面内明确标识的非语音说明音，案例段保留 GT 音轨。这个取舍在事实边界上是正确的，也足以完成申请展示。若后续寻求更强的现场感染力，可按 [narration.zh-CN.md](../docs/grant/video/v2/narration.zh-CN.md) 录制真人中文旁白，并在案例段降到不遮蔽 GT；但不得把旁白或任何新声音标为模型输出。该建议不构成通过条件。

## 评分

| 维度 | 分数 | 严格判断 |
| --- | ---: | --- |
| 项目定位与申报适配 | 9.2 / 10 | “多模态智能视频配音 + 完整方法图谱 + 可交互可核查”的定位鲜明，且没有把整合误写为模型拼接。 |
| VTTS 任务表达 | 9.3 / 10 | 三输入、完整方法、两输出以及多模态同步约束在首页和影片中都足够直观。 |
| 交互可视化与专业度 | 9.2 / 10 | 任务流、观察层、同步时间线、方法 Canvas 和移动端表现成熟；动态镜头已进入成片。 |
| 样例、权利与事实边界 | 8.8 / 10 | 历史案例/GT/任务说明/Concept 的界限严谨，权利记录透明；原始来源链仍需受控证据补强。 |
| 影片叙事与展示效果 | 9.1 / 10 | 前 20 秒为真实动态交互，案例段有真实可见媒体与明确音轨边界，节奏、字幕和视觉层级专业；真人旁白可作为后续增强。 |
| 可复现交付与发布准备 | 8.7 / 10 | 构建、hash、清单、干净检出和测试充分；远端正式 tag 及原始来源受控证明尚未收口。 |
| **总分** | **9.1 / 10** | **达到 9 / 10。作为申请冻结候选通过；远端正式发布须先完成两项 P1。** |

## 发布与申报措辞

在完成 P1 前，申报材料可以如实写为：

> OpenDub V2 已形成可交互的视频配音任务图谱、完整方法展示与可追溯历史样例；本次申报重点支持其统一展示、可视化解释、证据治理和后续可复现接入能力。

不得写为：

> 已经发布可在线实时生成、可公开公平比较的统一视频配音模型。

完成 P1、推送正式 tag 后，才可在公开页面将版本标为 `v2.0.0-showcase` 正式发布版本。
