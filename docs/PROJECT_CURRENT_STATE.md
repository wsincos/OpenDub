# OpenDub 项目当前状态说明

**更新时间：** 2026-07-26
**功能实现提交：** `b490056`（本说明随后以 `8b77b94` 补充）
**主仓库：** <https://github.com/wsincos/OpenDub>

## 1. 先说结论

OpenDub 当前已经完成了一个可以用于申报展示和录制视频的 **Concept Atlas（交互式方法图谱）版本**。

这个版本已经能够清楚地说明视频配音生成是什么、三个团队已有方法分别解决什么问题、它们的完整流程是什么，以及目前哪些能力已经有证据、哪些能力还不能声称已经运行。

但是，以下两件事**还没有完成，也没有被伪装成已完成**：

1. 同一输入下的真实多方法音频对比（Replay Comparison）。
2. 用户上传新视频后现场运行模型生成语音（Live Generation）。

原因不是界面没有做好，而是目前公开 checkpoint 还没有同时满足权重使用条款、SHA-256 校验、可复现运行环境、授权素材和真实 smoke test 等条件。OpenDub 的页面会明确显示这一事实。

因此，更准确的表述是：

> **OpenDub 已完成可录制、可交互、可追溯的三方法视频配音生成 Concept Atlas；真实 Replay 和 Live 生成保留为证据通过后的升级能力。**

## 2. OpenDub 是什么项目

建议对外项目名称：

> **OpenDub：面向视频配音生成的交互式方法图谱、可视化比较与开源复现平台**

OpenDub 不是把多个论文仓库简单放在一个网页上，也不是把不同论文的网络模块拆开后重新拼成一个未经验证的新模型。

它做的是：

1. 用直观方式解释视频配音生成任务；
2. 将已有的完整方法做成可点击、可观察、可比较的交互图谱；
3. 为未来真实运行、结果回放和公平比较建立统一的证据与数据规范。

### 视频配音生成任务

```text
Video + Text + Reference Voice -> Dubbing Method -> Target Speech
                                                  -> Dubbed Video
```

其中：

- `Video`：静音目标视频，提供口型、面部表情、场景等视觉条件；
- `Text`：要说出的台词；
- `Reference Voice`：经授权的参考语音，提供角色身份或声音风格；
- `Target Speech`：研究模型生成的目标配音语音；
- `Dubbed Video`：OpenDub 将目标语音与视频混流后的产品输出。

这与普通文本转语音不同。普通 TTS 主要解决“这段文字怎么念”；视频配音生成还需要回答“角色在这个画面、这个时刻、这个情绪下，应当以怎样的节奏和声音说出这句台词”。

## 3. 当前只使用的三个完整方法

首版公开 Method Atlas 只包含以下三套完整的视频配音生成方法：

| 方法 | 论文 | 核心问题 | 在 OpenDub 中的专属交互 |
|---|---|---|---|
| HPMDubbing | CVPR 2023 | 如何让 Lip、Face、Scene 三个视觉层级共同约束配音韵律 | 分层韵律视图：切换 Lip、Face、Scene，理解它们分别影响时长、音高/能量和全局情感 |
| StyleDubber | Findings of ACL 2024 | 如何从视频帧级理解提升到音素级和话语级风格学习 | 多尺度视图：切换 Frame scale 与 Phoneme scale，观察局部发音和全句风格的关系 |
| EmoDubber | CVPR 2025 | 如何同时考虑同步、清晰度、身份和可控情感 | 情感引导视图：选择情感方向和强度，理解正负引导机制，但不会假装生成了新音频 |

`HPMDubbing_Vocoder`、预处理工具和媒体工具属于支持性基础设施，不被误写成第四个独立视频配音方法。

## 4. 已经完成的网页内容

### 4.1 Task Explorer：解释任务本身

入口：`/explore`

这是录制视频的最佳起点。页面用输入、完整方法和输出三列结构说明：

- Video、Target Text、Reference Speech 三项输入分别提供什么信息；
- 为什么视频配音不是“只输入文字”的 TTS；
- `Generated Speech` 与 `Dubbed Video` 为什么是两个不同概念；
- Scene、Face、Lip 等视觉线索为什么重要；
- 用户随后可以进入三种完整方法的图谱。

页面中的波形和频谱使用 `Concept` 状态标记，不声称它们是当前模型实时生成的结果。

### 4.2 Method Atlas：展示三项研究工作的连续性

入口：`/methods`

这个页面将 HPMDubbing、StyleDubber、EmoDubber 组织成一条研究演进线，而不是三个没有关联的仓库卡片。每个方法都显示：

- 会议与年份；
- 研究问题；
- 方法贡献；
- 当前内容状态；
- 可点击进入的方法页、论文和源码入口。

### 4.3 Method Canvas：完整方法的可点击图谱

入口：

- `/methods/hpmdubbing`
- `/methods/styledubber`
- `/methods/emodubber`

每个方法页都已经具备：

- 从 manifest 读取的全部节点，而不是只画一条装饰性流水线；
- 论文中定义的真实信息边和分支汇合关系；
- 可点击组件，例如 Reference Speech、Lip Motion、MPA、PLA、LPA、PE、FUEC、PNGM；
- 组件检查器：说明该模块解决什么问题、可以观察哪些信号、页面当前属于什么内容状态；
- Signal Dock：用户可固定组件声明的可观察信号；
- Paper、Source 和 Evidence 入口；
- 适合移动端的水平图谱浏览和适合桌面录屏的完整画布。

### 4.4 三种专属 Concept Lab

三个方法页下方都有与论文主题对应的交互内容：

#### HPMDubbing：Hierarchical Prosody Lens

```text
Lip motion   -> duration / local timing
Face affect  -> pitch + energy / local expression
Scene affect -> global emotion / utterance context
```

用户点击不同视觉层级时，解释、关系高亮和示意信号会变化。示意信号明确标记为 `ILLUSTRATIVE SIGNAL`。

#### StyleDubber：Multi-scale Alignment Lens

用户可以在 `Frame scale` 与 `Phoneme scale` 之间切换，理解为什么多个视频帧需要对应稳定的音素区间，以及为什么 USL 代表全句级风格，而不是普通的局部特征。

#### EmoDubber：Emotion Guidance Lens

用户可选择 `Warm`、`Tense`、`Melancholic` 等概念情感方向，也可以调整概念强度。页面始终显示：

> `No new audio generated in Concept mode.`

因此这个交互解释了情感控制机制，但不会把滑杆变化伪装成模型刚刚生成的新声音。

### 4.5 Evidence Room：所有公开主张都能追溯

入口：`/evidence`

Evidence Room 是本项目可信度的重要部分。它为每个核心方法显示：

```text
Paper -> Source revision -> Code license -> Weight terms
      -> Runtime status -> Public content status
```

当前三种方法的共同事实是：

- 论文和固定源码 commit 已记录；
- 源码许可证为 MIT，已在上游审计中记录；
- 权重条款未核验；
- 运行时状态是 `unavailable`；
- 当前公开内容是 `Concept only`。

页面还展示了进入 Live 的完整门槛：固定源码、许可证、权重条款、SHA-256、隔离环境 smoke test 和可公开 Replay，缺少任何一项都不能把模型标记为 Live。

### 4.6 Comparison Lab：不伪造比较结果

入口：`/compare`

Comparison Lab 的界面已完成，但当前处于 `EVIDENCE-GATED` 状态。它展示：

- 公平比较必须使用同一个视频、同一台词、同一参考语音、同一时间范围；
- 需要素材权利、统一时间基准和音量策略；
- 三个方法都还没有可公开的同输入 Replay Bundle；
- 因此不会显示假 A/B 音频、假指标或“哪个方法最好”的结论。

这比在申报视频中播放来源不明的 Demo 更可信，也更符合开源项目的长期要求。

## 5. 为项目准备的文档和规划

`TODO/` 是后续继续开发、补充真实模型和制作申报材料的规划中心。

最重要的三个入口是：

1. [范围锁定与产品决策](../TODO/00_PRODUCT/SCOPE_LOCK_AND_PRODUCT_DECISION.md)：为什么采用“三个完整方法 + 可视化与比较层”的方式。
2. [三方法交互体验规格](../TODO/01_CAPABILITIES/METHOD_EXPERIENCE_SPEC.md)：每个方法应该怎样展示、哪些互动允许、哪些不允许。
3. [从零启动执行手册](../TODO/03_EXECUTION/START_HERE.md)：后续重新启动开发时应按什么顺序执行、每一步如何验收。

另外已经准备好：

- 任务定义、产品视觉规范、系统架构和数据契约；
- 模型能力与信号可视化规范；
- 内容状态规则：`Concept`、`Replay`、`Live`、`Planned`；
- 申报叙事、影片脚本、镜头清单、录制流程和事实核验规则；
- 许可、素材、checkpoint、风险和团队协作规范。

## 6. checkpoint 与真实模型的当前情况

已经对 HPMDubbing、StyleDubber、EmoDubber 的官方公开 checkpoint 候选进行了审计，详细记录在：

[checkpoint-audit-2026-07-26.md](atlas/checkpoint-audit-2026-07-26.md)

审计发现：部分 Google Drive 文件可以被发现或读取到文件名、大小，但没有同时具备以下必要条件：

1. 明确的权重使用和展示条款；
2. 发布方给出的 SHA-256；
3. 与源码提交匹配的可复现环境；
4. 已授权的视频、文本和参考语音测试样例；
5. 隔离环境中的真实推理 smoke test。

因此当前决定是：

- 不下载或镜像这些权重到公开仓库；
- 不把它们接入网页中的 Live 按钮；
- 不用来源不明或受版权限制的影视素材制作公开 Replay；
- 等满足全部条件后，再从一个完整方法开始升级为 Live。

这不是功能缺失，而是项目主动保留的真实性和合规边界。

## 7. 如何演示和录制视频

本地开发服务当前可从下面地址打开：

<http://127.0.0.1:5173/explore>

推荐录制顺序：

1. 打开 `/explore`，先解释 Video + Text + Reference Voice 如何共同决定目标语音。
2. 进入 `/methods`，说明团队不是只有一篇工作，而是三套完整、连续演进的方法。
3. 进入 HPMDubbing，点击 Lip、Face、Scene，展示分层视觉韵律的特点。
4. 进入 StyleDubber，切换 Frame scale 和 Phoneme scale，展示多尺度风格学习。
5. 进入 EmoDubber，调整情感方向和强度，强调这是机制解释而不是伪造的实时音频。
6. 打开 `/evidence`，证明源码、许可证、权重和运行状态都有清晰边界。
7. 最后打开 `/compare`，说明公平比较在缺少同输入真实结果时不会强行排名。

完整的镜头、旁白和后期要求位于：

[TODO/04_OPEN_SOURCE/DEMO_FILM](../TODO/04_OPEN_SOURCE/DEMO_FILM/README.md)

## 8. 当前代码结构

```text
apps/web/
  src/features/explore/      Task Explorer
  src/features/methods/      Method Atlas、完整图谱、Concept Labs
  src/features/compare/      Evidence-gated Comparison Lab
  src/features/evidence/     Evidence Room
  src/content/methods.ts     前端方法 manifest 读取和图谱布局

content/methods/
  hpmdubbing/method.json
  styledubber/method.json
  emodubber/method.json      三个方法的结构化内容来源

src/opendub/atlas/
  models.py                  方法、信号、Replay 等数据校验模型
  validation.py              manifest 校验逻辑

TODO/
  产品、交互、架构、质量、申报与影片规划

docs/audits/
  上游源码、许可证、运行条件和风险审计
```

## 9. 已完成的验证

最近一次验证结果：

| 检查项 | 结果 |
|---|---|
| Python 测试 | `98 passed`，仅保留一个上游依赖弃用警告 |
| 前端组件测试 | `13 passed` |
| 三份方法 manifest | `3 method manifests validated` |
| 前端生产构建 | 成功 |
| 视觉检查 | 已检查 `/explore`、`/methods`、三张方法页、`/compare`、`/evidence` 的 `1440x900` 与 `390x844` 布局 |
| GitHub 推送 | 已推送至 `main`，commit 为 `b490056` |

## 10. 后续真正需要做什么

录制申报视频前，当前版本已经可以使用。若后续继续开发，建议顺序如下：

1. 请方法作者或负责人复核三个方法图谱的节点、边和文字表述。
2. 固定一个发布 commit，按影片制作包完成录屏、旁白、字幕和事实核验。
3. 寻找并审核可以公开使用的同输入 Replay 结果；只有这样才能开放真实 A/B/C 对比。
4. 等权重、哈希、授权样例和隔离环境齐备后，选择一套完整方法接入 Live。
5. Live 成功后再将真实中间信号导入图谱和 Signal Dock，不能用 Concept 信号代替。

## 11. 一句话总结

> OpenDub 当前已经是一套可以清楚展示“什么是视频配音生成、团队已有三套完整方法各自有什么特点、当前证据到了什么程度”的专业交互式开源项目；它已经适合录制申报视频，但不会虚构真实模型运行、音频对比或 checkpoint 可用性。
