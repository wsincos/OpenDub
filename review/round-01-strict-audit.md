# OpenDub 青年开源种子计划严格审核（第 1 轮）

**审核日期：** 2026-07-26
**审核角色：** 独立、严格的青年开源项目评审
**审核对象：** `OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台`
**审核口径：** 评估当前提交物是否可作为种子计划的正式申请材料，而非评估其未来路线图是否有吸引力。

## 结论先行

**本轮总分：8.0 / 10，未达到 9 / 10 的提交门槛。**

这是一个定位清楚、视觉完成度高、技术表述罕见地克制且可信的申报版 Alpha。它已经不是“把几篇论文和几个仓库摆在一起”的目录：Task Explorer、三套完整方法的可点击 Canvas、Evidence Room、方法选择记录、授权输入与准备清单，构成了可演示的产品闭环。

但此时还不能按“已可正式提交”的标准给出 9 分，原因不在于没有把 `Concept` 伪装成 `Live`，恰恰相反，Concept 边界处理得很好。阻碍提交的是两项基本交付没有闭环：**申报所指向的 GitHub 远端没有包含当前申报版实现**，以及**申报视频尚只有脚本、没有实际成片/可访问链接**。这两项不完成，外部评审无法独立复核你展示的版本，也无法获得申请材料要求的视频证据。

## 评分

| 维度 | 分数 | 严格审核意见 |
| --- | ---: | --- |
| 申请叙事 | 8.3 | 项目名称、任务定义、边界和阶段目标一致；但“平台如何帮助用户按需求选择方法”的选择依据还没有形成一个一眼能懂的引导面。 |
| 差异化 / 创新 | 8.8 | “完整方法而非内部模块拼装”与“证据默认进入工作流”是清晰且值得申报的差异点；不是凭空宣称一个新模型。 |
| 交互与专业感 | 8.9 | Task Explorer、Method Canvas、Evidence Room 具备专业的研究工具视觉语言，方法机制也确实可以交互查看；中文评审现场的语言可达性仍可加强。 |
| 用户路径可用性 | 7.4 | `理解 -> 选择 -> 授权准备 -> 导出` 可以运行；但按需求选择的决策引导较弱，且 Studio 首页偏稀疏，当前路径没有可展示的授权 Replay 成果。 |
| 技术真实性 / 证据 | 8.2 | 本地证据链很强，未夸大 Live；但申报文档引用的远端仓库尚未发布本轮核心改动，外部可核验性被明显削弱。 |
| 申报交付物 / 演示力度 | 5.8 | Word、架构图、脚本已准备；正式申报视频尚未录制或链接，无法证明录屏叙事与本地页面是一致的。 |
| **总分** | **8.0** | **未达到 9 / 10。** |

## 已核验的优点

### 1. 项目定位成立，且没有做成“论文拼接模型”

- [README.md](../README.md)、[平台定位](../TODO/00_PRODUCT/PLATFORM_POSITIONING.md) 和 [申报摘要](../docs/grant/project-summary.md) 对外名称、输入输出和边界一致。
- `Video + Target Text + Authorized Reference Speech -> one complete method -> Target Speech -> Dubbed Video` 清晰解释了视频配音相较普通 TTS 的差异。
- 三个核心方法被保留为完整方法：HPMDubbing、StyleDubber、EmoDubber；[范围锁定](../TODO/00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md) 明确禁止跨论文内部模块拼装。这是本项目最重要的学术和工程可信度来源。

### 2. 交互展示具备“申请现场可见”的专业度

2026-07-26 使用真实 Chromium 访问本地 Web 端并检查：

- `/explore`（1440×1000、390×844）：输入、完整方法、输出和同步时间线结构清楚；Concept 波形与频谱有可见状态标记。
- `/methods`：三种方法不是卡片堆叠，而是有研究问题、方法路径、论文/源码和 `Prepare project` 的一致工作流。
- `/methods/emodubber`：可点击节点、右侧组件检查器与情感引导专属互动形成了清晰的机制解释。页面明确写有 `Concept explanation`，没有把滑杆伪装成新生成音频。
- `/evidence`：固定 source revision、代码许可证、权重条款、运行状态和进入 Live 的门槛同屏可见，是最能建立信任的页面。
- `/compare`：在没有合格共用输入结果时显示 `0 / 3 verified replay bundles` 与 `Zero invented outputs`，比伪造音频或指标更适合严肃申请。
- [架构图](../docs/architecture/opendub-platform-architecture.svg) 在 Chromium 中渲染正常，准确展示 Atlas、Studio 和证据门控，而没有误画成融合神经网络。

### 3. 真实性和工程质量有实际依据

- 运行 `make check`：Ruff 格式与静态检查通过、Mypy 通过、`108 passed`；仅有已知的 Starlette TestClient 弃用警告。
- 运行 `pnpm --filter @opendub/web test -- --run`：`11` 个测试文件、`21` 项测试通过。
- 运行 `pnpm --filter @opendub/web build`：Vite 生产构建通过。
- 运行 `opendub atlas validate --content content`：`3 method manifests validated`；模型 Registry 校验通过；`git diff --check` 无空白错误。
- [申报证据索引](../docs/grant/evidence-index.md) 能把“已实现”“条件升级”“待人工补充”分开，且 [checkpoint 审计](../docs/atlas/checkpoint-audit-2026-07-26.md) 没有把公开下载链接误写成可运行模型。
- [申报版 Word 表](../original/OpenDub_青年开源种子计划申报表_申报版_v0.0.1.docx) 经 LibreOffice 渲染为两页 A4，表格内容可读且没有版式溢出。

## 必须整改的问题

### P0-1：申报所链接的远端仓库没有本轮申报版实现

**证据：** 本地 `HEAD` 与 `origin/main` 均为 `3e82a76`，但工作区存在 47 个已修改文件及多项未跟踪文件。申报闭环所需的 [准备导出服务](../src/opendub/application/preparation_service.py)、[架构图](../docs/architecture/opendub-platform-architecture.svg)、Studio/选择持久化测试等尚不存在于 `origin/main`。远端 README 仍使用旧的 `Interactive Atlas for Video Dubbing Methods` 副标题，且没有本轮的 P1/P2/P3 申报版内容。

**影响：** Word 表与 README 指向 `https://github.com/wsincos/OpenDub`，但评审点击后无法核验本地展示的“方法选择、授权输入、准备导出、申报架构图”等核心主张。这是申报可信度问题，不是代码风格问题。

**整改：**

1. 清点并只纳入申报版所需的实现、测试、文档、架构图、Word 副本与素材许可证；不要把 `reference/` 这类工作材料误提交。
2. 运行完整质量门并形成一次清晰的申报冻结提交；推送 `main`。
3. 创建可复核的 `v0.0.1-alpha.0` 标签或 GitHub Release，Release Notes 应明确 `Concept`、`Replay`、`Live` 边界和验证命令。
4. 从无本地未提交改动的全新 clone 按 [Local Alpha Quick Start](../docs/getting-started/local-alpha.md) 复跑关键路径，并记录 commit/tag。

**验收：** 远端仓库能看到当前 README、`preparation_service.py`、架构图与测试；Release/tag 的提交 SHA 与申报 Word 和视频中出现的版本一致。

### P0-2：正式申报视频尚不存在，Word 也没有可访问的视频交付物

**证据：** [演示脚本](../docs/grant/demo-script.md) 是完整的 95–110 秒录制计划，但 [项目当前状态](../docs/PROJECT_CURRENT_STATE.md) 和 Word 的“项目演示视频”栏均写明“正式录制按脚本执行”。这说明视频还不是当前交付物。

**影响：** 此类申请的视觉说服力主要来自短视频。脚本不能替代已录制的、与当前发布提交对应的成片；表格注释也要求提供视频/技术文档的在线链接或随申请上传。

**整改：**

1. 以 P0-1 的冻结 commit/tag 启动录制；录制 `95–110` 秒、`1920×1080`、30 FPS 的最终版。
2. 使用可公开的中文旁白和中文/英文双语字幕；在第 0–20 秒明确任务输入输出，在第 20–55 秒展示三方法差异与一个 Canvas，在第 55–80 秒展示 Studio 准备导出，在第 80–100 秒展示 Evidence Room 与边界。
3. 在片尾显示项目名称、仓库 URL、tag/commit、Apache-2.0 与“Concept / no Live runtime”边界；将视频文件或可公开访问链接填入 Word 相应字段。
4. 按 [证据索引](../docs/grant/evidence-index.md) 逐句事实核对，确保不把图示、预设波形、准备清单或上游 Demo 说成现场生成。

**验收：** 有一份最终 MP4/在线链接、SHA-256、字幕文件和录制版本记录；独立审核者可从视频进入远端仓库并复现每个展示页面。

## 应在本轮尽量完成的强化项

### P1-1：把“选择完整方法”从跳转按钮升级为按需求的可解释决策

**证据：** [Method Atlas](../apps/web/src/features/methods/MethodAtlasPage.tsx) 已有三项 `Prepare project`，但用户需要自行读完三张卡片才能判断选择条件。申报文案称“帮助创作者和开发者选择一个完整方法”，实际 UI 尚未把“我的首要需求是什么”变成直接入口。

**整改：** 在 `/methods` 首屏或 Task Explorer 到 Methods 的过渡处加入一个非常小的 “Choose by need” 引导：

- `Visual prosody / scene rhythm` -> HPMDubbing；
- `Local pronunciation + global character style` -> StyleDubber；
- `Explicit emotion direction` -> EmoDubber。

结果只能写“适合优先理解/准备的方法”，不得写“全局最优”或“已能生成”。应保留进入 Evidence 和 `Prepare project` 的两个明确后续动作。

**验收：** 评审无需阅读论文也能在 10 秒内理解三方法的选择差异；新增交互有测试，文本保留 Concept 与 runtime 边界。

### P1-2：为中文项目申请提供中文演示可达性

**证据：** Method Manifest 已含 `zh_cn`，但当前 Web 首屏、方法图谱、Evidence Room 和 Studio 主要是英语界面。英文研究工具风格本身专业，但会增加中文评审在 100 秒视频里的理解成本。

**整改：** 最小可行方案不是全量国际化，而是：增加简体中文演示模式，或至少在申请录制路径提供固定中文 UI/双语浮层、中文方法选择引导和中文字幕。中文名称应在首屏与片尾明确出现。

**验收：** 中文评审不依赖英语即可说清三输入、三方法差异、Concept 边界和准备导出的意义。

### P1-3：让 CI 的真实门禁与申报中的质量声明一致

**证据：** 当前 [CI](../.github/workflows/ci.yml) 只运行 `make check`；而 `make check` 的 `web-check` 仅执行 TypeScript 检查，不执行 Vitest 或 Vite 生产构建。虽然本次人工复核中二者均通过，但 [项目当前状态](../docs/PROJECT_CURRENT_STATE.md) 的“前端测试与生产构建通过”不会被每次 CI 自动保证。

**整改：** 在 `package.json` / Makefile / CI 中把前端 `test -- --run` 与 `build` 纳入同一个强制门禁，或创建独立 Web CI job。保留日志/徽章/Release Notes 中的验证摘要。

**验收：** 在全新 CI 运行中能看到前端类型检查、21 项以上组件测试与生产构建均成功。

### P1-4：在不伪造模型输出的前提下补足“视频配音”的结果锚点

**评估边界：** 没有 Live checkpoint 不应扣成“项目不成立”；当前 Concept 边界是优点。但项目名称含“视频配音平台”，演示中完全没有一段有权利、可追溯的声音/视频结果，会使部分评审感到产品只停留在说明层。

**整改路径（仅满足证据门槛后采用）：** 为任一完整方法建立一个 `Replay`，而非伪造 Live：取得明确授权的短视频、台词、参考语音和历史输出，记录输入/输出 SHA-256、来源、方法 commit、许可和结果说明；在页面上永久标为 `Replay`、`not a fresh OpenDub run`。若无法取得全部权利，则不展示任何音频，并在视频中强化“种子支持用于完成首个受控 Replay/Live 准入”的价值。

**验收：** 有合格 Replay 时可播放且每个来源可追溯；无合格 Replay 时视频和 Word 不暗示已有播放结果。

## 可后置但会提升完成感的问题

### P2-1：Studio 首页的视觉张力和引导不足

`/studio?method=emodubber` 的“Method preselected”提示正确，但项目首页在空项目/单项目状态下大面积留白，研究工作台的密度和叙事强度弱于 Atlas。录制时应从 Canvas 的 `Prepare project` 直接进入，避免将首页作为长镜头；后续可把“选择的方法、授权状态、下一步”做成紧凑的进度面板。

### P2-2：版本发布材料还可再正式化

当前版本为 `v0.0.1-alpha.0` 是诚实的，但应补一个简短 `CHANGELOG.md` 或 GitHub Release Notes，写清本版本新增的 Atlas、选法记录、准备导出和限制。这样评审看到的不是工作区快照，而是可被引用的开源版本。

### P2-3：术语在申请材料中可以更面向非技术评审

Word 中的 `Method Manifest`、`preparation manifest`、`adapter`、`smoke test` 等术语准确但密集。首处应在中文后加 4–8 字解释，例如“方法说明清单”“可复现准备清单”“运行适配器”“最小真实运行验证”，其余位置再沿用英文。

## 不应作为整改项的内容

以下不是本轮扣分原因，也不应为了“炫酷”而破坏：

- 不应把 HPMDubbing、StyleDubber、EmoDubber 的内部模块拼成一个未经验证的 OpenDub 新模型。
- 不应把论文图、概念波形、情感滑杆、公开视频 Demo 或测试音频包装成“当前模型现场生成”。
- 不应在没有同输入、同权利、同时间基准的前提下给三种方法排“最佳”。
- 不应为了补一段配音效果而使用未获授权的影视片段、真实人物声音或来源不明 checkpoint。

## 达到 9 / 10 的下一轮硬性验收项

下一轮必须同时满足以下条件，才可给出 `>= 9 / 10`：

1. **远端一致性：** 当前申报实现和文档已推送，且用无本地改动的新 clone 按文档复现；存在可引用 tag/Release。
2. **视频交付：** 有最终录制视频或稳定公开链接，Word 中填入该链接/附件说明；视频与 Release 使用同一版本标识。
3. **视频叙事：** 视频能在两分钟内清楚回答“任务是什么、三个完整方法如何不同、用户为何能选择、Studio 实际保存什么、为什么当前不做假 Live”。
4. **选择体验：** 在交互界面中提供可解释的按需求选择引导，绝不声明“全局最优”。
5. **质量门禁：** CI 自动覆盖 Python 静态检查/测试、Web 类型检查/组件测试/生产构建、Manifest/Registry 和文档链接。
6. **事实边界：** `Concept`、`Replay`、`Live` 的标签和申请文字保持一致；没有未经证据准入的音频、指标、排名或模型可用性主张。

完成 P0-1、P0-2、P1-1、P1-2、P1-3 后，即使仍不具备 Live checkpoint，只要上述事实边界继续成立，本项目可达到 **9.0–9.2 / 10 的种子计划申请水平**。合规的单方法 Replay 会进一步增强视频配音任务的结果感，但不是通过本轮 9 分门槛的前置条件。
