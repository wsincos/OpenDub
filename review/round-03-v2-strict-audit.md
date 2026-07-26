# OpenDub V2 严格申报审核（第 3 轮）

**审核日期：** 2026-07-27
**审核角色：** 独立严格审核者（不参与实现）
**审核对象：** `OpenDub v2.0.0-showcase` 当前工作树、`/vtts`、`/examples`、`/methods`、`/studio`、`/evidence` 与 V2 申报片
**结论：** **不通过，当前 7.8 / 10，未达到 9 / 10 发布和申报影片门槛。**

本轮没有发现把历史案例、GT 音轨、任务示意或 `Concept` 方法伪称为 fresh run、Replay 或 Live 的问题。相反，案例状态、没有 canonical transcript / IPA 的事实、以及任务示意的边界都处理得相当克制。这是本版本最强的部分。

不过，当前交付还不能称为“可发布的 V2”：视频实际是以静态网页截图为主、影片中出现 API 错误页、交付 manifest 的视频哈希已失配，并且仓库的标准 `make check` 失败。这些不是审美意见，而是可复现的发布阻塞项。

## Findings

### P0-1：V2 成片没有交付所承诺的动态任务演示，且约 80% 时长是无旁白的静态镜头

**证据：** [scripts/build_v2_showcase_film.sh](../scripts/build_v2_showcase_film.sh#L14) 的 `make_still` 用 `-loop 1` 把 PNG 变为视频，并在 [55-64 行](../scripts/build_v2_showcase_film.sh#L55) 对流程、线索、时间线、方法、Studio、Evidence 和结束画面连续调用。唯一运动的段落是两个四格案例视频。`silencedetect` 的实际输出表明影片在 `0-32.0997s` 和 `53.7344-106.225s` 静音；即 106.234 秒里约 **84.6 秒静音**。联系表及 0/12/24/36/48/60/72/84/96/106 秒抽帧也证实前三个任务阶段是静态页面。

这直接违反 V2 计划要求的“前 24 秒出现真实可读的数据流动画”和“不得以静态网页截图代替动态数据流段”（[04_FILM_V2_PRODUCTION_PLAN.md](../TODO/07_V2_SHOWCASE/04_FILM_V2_PRODUCTION_PLAN.md#L30)），也没有达到完成定义中的“展示动态任务”（[README.md](../TODO/07_V2_SHOWCASE/README.md#L67)）。当前网页本身有真正可暂停的数据包动效（[VttsTaskStagePage.tsx](../apps/web/src/features/vtts/VttsTaskStagePage.tsx#L48) 和 [119-130 行](../apps/web/src/features/vtts/VttsTaskStagePage.tsx#L119)），但成片没有录到它。

**必要修复：** 以正在运行的 `/vtts?tour=flow` 录制真实浏览器视频片段，至少覆盖三输入依次流入完整方法、双输出出现、Face/Lip/Environment 切换和时间线播放头推进；不要用静帧停留来替代。加入清晰的人工中文旁白或经过明确标注的说明音轨；在真实 GT 样例段降低旁白并保留 `AUDIBLE: GT`。重新抽帧、试听并更新字幕、contact sheet、哈希和 manifest。

### P0-2：Studio 镜头和当前实际 `/studio` 都显示 `Local API unavailable`，与影片“可记录、可导出”的叙事冲突

**证据：** 当前 `http://127.0.0.1:5181/studio` 桌面核查显示红色 `Local API unavailable / Failed to fetch`。`127.0.0.1:8000` 的 `/health` 与 `/api/projects` 均为连接拒绝；Vite 端口上的 `/api/projects` 返回 HTML 而不是 API 响应。V2 联系表和 [assets/screens/08-studio.png](../docs/grant/video/v2/assets/screens/08-studio.png) 也把该错误画面放入成片。与此同时，旁白稿称“在本地 Studio 中，方法选择、输入授权和证据版本会被共同记录”（[narration.zh-CN.md](../docs/grant/video/v2/narration.zh-CN.md#L12)）。

这不是“当前未接入模型”的诚实边界，而是正在展示的已有工作流失败。它会使评审合理怀疑 Studio 与准备导出并不可用。

**必要修复：** 启动可工作的本地 API，并以可复现的启动命令和健康检查验证从 `/studio` 创建本地项目、记录准备信息、导出 manifest 的完整路径；重新录制 Studio 镜头，成片中不得出现错误状态。若无法在本轮提供 API，删去 Studio 可操作性和导出能力的镜头/旁白，只保留如实可运行的 Atlas、Examples 和 Evidence 范围。

### P0-3：视频完整性清单失配，且 V2 仍未进入可引用的提交或 tag

**证据：** [delivery-manifest.json](../docs/grant/video/v2/delivery-manifest.json#L7) 声称 MP4 SHA-256 为 `5b11e6...`；实际文件及 [OpenDub_VTTS_Showcase_v2.0.0.sha256](../docs/grant/video/v2/OpenDub_VTTS_Showcase_v2.0.0.sha256#L1) 为 `55ebd5...`。独立计算确认前者 `MATCH=False`，而 SRT 和旁白稿哈希匹配。`git status --short` 显示所有 V2 源码、案例和 `docs/grant/video/v2/` 仍是未跟踪文件；`HEAD` 仅为 V1 `a3e40f7`，没有 V2 tag。

**必要修复：** 每次重建后在同一脚本或校验命令中更新并验证 delivery manifest 的所有哈希；将 V2 需要公开的媒体显式纳入版本控制或 Git LFS，完成 scoped commit、干净 clone、公开视频和视频校验，再建立 `v2.0.0-showcase` tag。提交前不得把目前的 manifest 当成可核验交付物。

### P1-1：标准质量门 `make check` 当前失败，文档的“已通过”记录不准确

**证据：** 运行 `make check` 在 `format` 第一步失败：`src/opendub/showcase/features.py` 需要 Ruff 格式化（两处生成器换行，[features.py](../src/opendub/showcase/features.py#L45) 与 [79 行](../src/opendub/showcase/features.py#L79)）。[Makefile](../Makefile#L6) 正是将此命令定义为发布质量门；但 [PROJECT_CURRENT_STATE.md](../docs/PROJECT_CURRENT_STATE.md#L129) 声称 Python 格式检查已经通过。单独运行的 `pytest`（116 passed）、mypy、ruff lint、registry、case `--verify-only` 和 web build 均通过，不能替代失败的正式门禁。

**必要修复：** 运行 formatter 并提交结果；从干净工作树完整执行 `make check`、两条 showcase verify、registry、`ffprobe`、`sha256sum -c` 与 manifest-hash 交叉检查。只有命令真实通过后，才在状态文档将对应项标为完成。

### P1-2：再分发权利和样例输入合同具有自声明边界，不能被写成“独立已核验的公开许可”

**证据：** 两个 case 都把 `rights.video`、`rights.reference_speech` 写为 `confirmed-by-project-owner`，并把 `redistribution` 写为 `allowed-for-opendub-v2`（例如 [human-0.json](../content/showcases/v2/human-0.json#L8)）；但 case 同时明确缺 target text、canonical IPA 与 same-input 合同（[12-17 行](../content/showcases/v2/human-0.json#L12)）。页面和影片正确标记为 `Archived research example`，没有宣称公平比较或 Replay，这是正确的；但仓库没有可供外部评审复核的授权记录或受限资产替代方案。

**必要修复：** 在不公开身份、音频或敏感文件的前提下，加入可复核的授权声明/资产权利记录（权利主体、适用场景、允许公开范围和审批日期），或把媒体改成仅随申报包受控提供，并将公开站点替换为无敏感媒体的 poster/metadata。继续保持 `Archived research example`、禁止 compare 排名和 canonical IPA 声称。

### P2-1：规划、实施记录与验收清单之间仍有可避免的矛盾

**证据：** [V2 总览](../TODO/07_V2_SHOWCASE/README.md#L64) 把“真实 IPA 音素”写为完成定义，同时下一行又说明两个案例缺 canonical transcript / IPA；[实施记录](../TODO/07_V2_SHOWCASE/06_IMPLEMENTATION_RECORD.md#L45) 才准确解释页面 IPA 仅是 `task notation`。此外，质量计划的功能、视觉和发布项目仍全部未勾选（[05_V2_QUALITY_RELEASE_AND_AUDIT.md](../TODO/07_V2_SHOWCASE/05_V2_QUALITY_RELEASE_AND_AUDIT.md#L13)），与当前状态文档的多项“已完成”表述难以区分。

**必要修复：** 统一计划、实施记录和项目状态：明确“真实 GT 声学特征 + task notation IPA”，不要出现“真实 case IPA”字样；只对已执行且记录了证据的门禁打勾。保留未发布、未 Live、未 Replay 的状态。

## 已核查的正面事实

- `/vtts` 在 1920x1080 与 390x844 下均没有文字重叠；窄屏导航折叠正常。任务阶段把 Video、Target Text、Authorized Reference Speech、完整方法、Target Speech 和 Dubbed Video 的关系讲得清楚，且数据包动画有播放、暂停、重置控制。
- `/examples` 的 Human/Animated 两个 tab 和 GT/HPMDubbing/StyleDubber/EmoDubber 四面板均可访问，媒体资源返回 200；界面固定写明 `Archived research example. Not a fresh OpenDub run.`，未出现分数、排名或“best”暗示。
- `/methods` 和 EmoDubber Canvas 清晰维持“complete methods, not mixed internals”的定位；`/evidence` 诚实显示三种方法为 `Concept only` / `Runtime unavailable`。
- `/vtts` 把英文 IPA 标为 `Illustrated IPA timing notation`，且 [实施记录](../TODO/07_V2_SHOWCASE/06_IMPLEMENTATION_RECORD.md#L45) 明确说明它不是两个历史案例的转写。这个边界足以避免把缺失 canonical transcript / IPA 包装成真实对齐。
- 核验通过：`pytest -q` 为 116 passed（1 个上游弃用 warning）、mypy 76 个源文件通过、ruff lint 通过、3 个方法 manifest 和 registry 通过、两组 showcase `--verify-only` 通过、前端 25 个测试和生产 build 通过。V2 MP4 本身也有 106.234 秒、1920x1080、H.264/AAC、嵌入 `mov_text` 字幕流，且 `OpenDub_VTTS_Showcase_v2.0.0.sha256` 与文件本身匹配。

## 评分

| 维度 | 分数 | 严格判断 |
| --- | ---: | --- |
| 项目定位与资格 | 8.6 / 10 | “完整方法图谱而非伪统一模型”的定位、AIGC 应用价值和下一阶段门槛清楚；但公开样例权利仍主要是自声明。 |
| VTTS 任务表达 | 9.1 / 10 | 三输入、一完整方法、两个输出，及 Face/Lip/Environment 的解释很清晰；IPA 的任务示意边界也诚实。 |
| 交互可视化专业度 | 8.8 / 10 | `/vtts`、Examples 和方法 Canvas 在桌面/移动端有成熟的信息层级和真实特征锚点；Studio 失败状态拉低端到端完成度。 |
| 真实样例与证据边界 | 8.7 / 10 | 历史案例/GT/任务示意/Concept 的表述严格，且不做伪比较；正式再分发权利和输入合同还不足以做公开、可独立审计的证明。 |
| 视频叙事与专业感 | 5.4 / 10 | 有真实案例、明确 GT 音轨和好看的静态构图，但大段静音静帧、未录到数据流和 Studio 错误页，不符合本轮“专业、炫酷、震撼”的要求。 |
| 可发布性 | 6.3 / 10 | 单项测试多数通过，但 `make check` 失败、delivery manifest 失配、V2 未提交/tag，不能发布。 |
| **总分** | **7.8 / 10** | **不通过；不得创建 V2 tag 或将当前 MP4 作为正式申请影片。** |

## 重新送审门槛

下轮只在以下全部具备后重新评分：

1. V2 影片使用真实浏览器录制的动态流程和可见交互，不再由静态网页 PNG 填充任务、线索和方法段；非样例段有符合字幕的中文旁白或明确说明音轨。
2. Studio 镜头来自实际可用 API 路径，能完成至少一次“创建项目 -> 记录/准备 -> 导出”验证；或删除该未可用能力的所有影片与文案声称。
3. `delivery-manifest.json` 与 MP4/SRT/旁白稿的 SHA-256 一致，并有自动校验命令；影片抽帧、声音、字幕与事实边界复核完成。
4. `make check`、case verify、registry、web build、`ffprobe`、媒体 hash 全部从干净树通过；状态文档只记录真实结果。
5. V2 源码和授权允许公开的媒体已提交到可引用 commit/tag，并通过干净 clone 访问页面、样例和影片。若权利材料仍只适用于申报包，公开站点必须移除受限媒体。

完成后，请基于新 commit、运行中的 API 和新 MP4 重新提交第 4 轮审核。
