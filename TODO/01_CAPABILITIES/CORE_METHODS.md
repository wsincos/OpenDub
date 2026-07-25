# Core Method Content Specifications

本文定义三套核心方法在 OpenDub 中必须呈现的结构。正式内容发布前必须由论文作者或项目负责人复核名称、边和语义。

## 统一展示骨架

三套 Method Canvas 使用相同信息层级，但保留各自架构：

1. Research Question
2. Inputs
3. Complete Method Flow
4. Observable Signals
5. Outputs
6. Evidence
7. Reproduction Status

统一骨架用于降低学习成本，不意味着方法内部结构相同。

## HPMDubbing

### 身份

- 完整名称：`Learning to Dub Movies via Hierarchical Prosody Models`
- 会议：CVPR 2023
- 方法 ID：`galaxycong/hpmdubbing`
- 核心问题：如何把 Lip、Face 和 Scene 三个视觉层级映射到语音韵律。
- 论文：`https://openaccess.thecvf.com/content/CVPR2023/html/Cong_Learning_To_Dub_Movies_via_Hierarchical_Prosody_Models_CVPR_2023_paper.html`
- 代码：`https://github.com/GalaxyCong/HPMDubbing`

### Canvas 主路径

```text
Text / Phonemes --------------------------+
Reference Speech -> Speaker Information --+--> Acoustic Representation
Lip Motion -> Duration Alignment ----------+
Face -> Valence/Arousal -> Pitch/Energy ---+
Scene -> Emotion Booster ------------------+
                                               |
                                               v
                                     Mel-Spectrogram
                                               |
                                               v
                                           Vocoder
                                               |
                                               v
                                        Dubbed Speech
```

### 可点击组件

| 节点 | 要解释的问题 | 输入 | 输出 | 推荐视觉 |
|---|---|---|---|---|
| Lip Motion | 嘴唇运动怎样限制语速和停顿 | Lip ROI、phonemes | duration/alignment | 口型帧条、音素块、对齐带 |
| Face Affect | 面部表情怎样影响局部韵律 | Face ROI | valence/arousal、pitch/energy 条件 | 人脸帧、VA 平面、F0/energy 曲线 |
| Scene Emotion | 场景氛围怎样提供全局情感 | Scene frames | global emotion embedding/condition | 场景缩略图、情感类别或概念轨 |
| Hierarchical Prosody | 三层视觉线索怎样汇合 | duration、pitch、energy、emotion | prosody-conditioned representation | 分层轨道合流，不画无依据热力图 |
| Mel Decoder | 韵律条件如何进入声学表示 | acoustic representation | mel-spectrogram | 时间对齐频谱 |
| Vocoder | 声学表示怎样转成可播放语音 | mel-spectrogram | waveform | mel 到 waveform 的确定性过渡 |

### Concept 模式

- 使用授权示例视频的帧、Face ROI 和 Lip ROI。
- duration、F0、energy 可以使用作者提供或预计算信号。
- 若只能使用示意数据，必须在轨道名称旁显示 `Illustrative`。
- 不伪造 attention heatmap。

### Replay / Live 升级

Replay Bundle 最少包含视频、文本、参考语音、目标语音、配音视频、音素时长、F0、energy 和 mel。Live 若能导出 valence/arousal 或场景情感，再启用相应真实信号层。

## StyleDubber

### 身份

- 完整名称：`StyleDubber: Towards Multi-Scale Style Learning for Movie Dubbing`
- 会议：Findings of ACL 2024
- 方法 ID：`galaxycong/styledubber`
- 核心问题：如何从 frame-level 转向 phoneme-level，在保持口型同步的同时提高发音、身份和多尺度风格表达。
- 论文：`https://aclanthology.org/2024.findings-acl.404/`
- 代码：`https://github.com/GalaxyCong/StyleDubber`

### Canvas 主路径

```text
Text -> Phonemes -------------------------------+
Reference Speech -------------------------------+--> MPA
Video / Facial Emotion -------------------------+
Lip Motion + Phonemes ------------------------------> PLA
MPA + PLA ------------------------------------------> Intermediate Embeddings
Intermediate Embeddings ----------------------------> USL
                                                        |
                                                        v
                                              Mel Decoder + Refinement
                                                        |
                                                        v
                                                   Dubbed Speech
```

### 可点击组件

| 节点 | 要解释的问题 | 输入 | 输出 | 推荐视觉 |
|---|---|---|---|---|
| Phoneme View | 为什么不直接按视频帧切分文字 | script | phoneme sequence | frame 网格与 phoneme 区间对照 |
| MPA | 如何在音素级融合参考发音风格和面部情感 | phonemes、reference audio、visual features | phoneme-level style representation | 三源输入汇入音素 token |
| PLA | 如何保持音素与口型同步 | lip motion、phonemes | aligned phoneme representation | 口型强度轨、音素边界、对齐连接 |
| USL | 如何在话语级保持整体风格 | intermediate embeddings | utterance-level style condition | 全句包络、全局风格带 |
| Mel Decoder | 如何生成声学表示 | conditioned embeddings | mel-spectrogram | 频谱逐段显现 |
| Post/Refinement | 如何细化输出 | preliminary mel | refined mel | 可切换前后频谱，但必须来自真实或论文证据 |

### Concept 模式

- 核心交互是 `Frame view` 与 `Phoneme view` 切换。
- 点击一个音素时，同步突出对应 Lip ROI 帧、参考语音区间和生成频谱区间。
- MPA 和 USL 分别使用局部与全局视觉尺度，不用同一动画重复表达。

### Replay / Live 升级

Replay Bundle 最少包含音素边界、Lip ROI、参考语音、目标语音和 mel。若无法导出 MPA/USL 内部表示，Concept 只解释信息流，不展示伪造数值。

## EmoDubber

### 身份

- 完整名称：`EmoDubber: Towards High Quality and Emotion Controllable Movie Dubbing`
- 会议：CVPR 2025
- 方法 ID：`galaxycong/emodubber`
- 核心问题：如何同时改善口型同步与发音清晰度，并允许用户控制情感类型和强度。
- 论文：`https://openaccess.thecvf.com/content/CVPR2025/html/Cong_EmoDubber_Towards_High_Quality_and_Emotion_Controllable_Movie_Dubbing_CVPR_2025_paper.html`
- 代码：`https://github.com/GalaxyCong/EmoDubber`

### Canvas 主路径

```text
Lip Motion + Phoneme Prosody -> LPA --------+
Video-level Phoneme Sequence -> PE ----------+--> Fused Sequence
Reference Speech -> Speaker Identity Adapting ---> Acoustic Prior
User Emotion Type + Intensity --------------------> FUEC / PNGM
Acoustic Prior -----------------------------------> FUEC / PNGM
                                                       |
                                                       v
                                                 Speech Waveform
```

### 可点击组件

| 节点 | 要解释的问题 | 输入 | 输出 | 推荐视觉 |
|---|---|---|---|---|
| LPA | 如何学习口型运动与韵律时长的一致性 | lip motion、phoneme prosody | aligned sequence | 正负时长对比、对齐轨 |
| PE | 如何在同步同时保持发音清晰 | video-level phoneme sequence、LPA output | enhanced phoneme sequence | 音素缺失/完整对照、单调路径 |
| Speaker Identity Adapting | 如何注入参考说话人 | reference speech、fused sequence | acoustic prior | 参考波形进入声学先验 |
| Emotion Control | 用户指定什么情感 | label、intensity | control condition | 情感 segmented control、0 至 1 强度 |
| FUEC | 如何生成受情感控制的语音 | acoustic prior、emotion condition | waveform trajectory/output | flow 轨迹概念视图和最终波形 |
| PNGM | 如何放大目标情感并抑制其他情感 | positive/negative guidance | guidance direction and scale | 双向矢量、强度变化试听 |

### Concept 模式

- 用户可操作情感类别和强度，但 Concept 控件只驱动解释动画或授权预计算结果。
- 未生成的新强度不得通过音量缩放伪装成情感生成。
- FUEC 的 flow 轨迹可以概念化，但必须标记 `Conceptual flow view`。

### Replay / Live 升级

Replay 最少包含多个真实情感类别或强度结果，才能启用可试听的情感控制。只有一条输出时，强度滑杆锁定并解释原因。Live 必须通过控制效果测试后才能开放任意强度运行。

## 方法间对应关系

Comparison Lab 可以按研究问题建立对应关系：

| 对比主题 | HPMDubbing | StyleDubber | EmoDubber |
|---|---|---|---|
| 口型与时长 | Lip Motion / Duration | PLA | LPA |
| 发音建模 | 基础 phoneme/acoustic path | MPA 的 phoneme-level learning | PE |
| 说话人/风格 | Reference/Speaker info | MPA + USL | Speaker Identity Adapting |
| 情感 | Face + Scene hierarchy | visual and utterance style | User Emotion + FUEC |
| 声学输出 | Mel + Vocoder | Mel + refinement + vocoder | Flow-based waveform path |

这些对应关系只用于导航和解释，不代表组件接口兼容。
