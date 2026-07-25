# Capability and Model Map

## 设计原则

用户购买的是能力，不是论文名称。OpenDub 将已有成果重新组织为稳定的产品能力，每个模型通过适配器声明自己支持的输入、控制和输出。一个模型可以支撑多个能力，一个能力也可以由不同模型实现。

## 七项产品能力

### 1. Visual Sync Engine

根据嘴部运动、视频时间窗和音素结构控制语音时长与节奏。

- HPMDubbing：分层建模口型、面部表情和场景信息，作为首要视频韵律参考。
- HD-Dub：面向层次音素建模和声学扩散去噪，代码已迁移到独立组织；通过许可与可复现核验后接入。
- CoSyncDiT：认知同步扩散 Transformer；当前 GalaxyCong 仓库仅有 README，代码与权重未形成可接入资产，因此列为 Planned。

### 2. Emotion Director

通过离散情感、强度或 valence/arousal 控制角色表达。

- EmoDubber：首选能力来源，承担 `v0.1.0` 第一个真实模型适配。
- HPMDubbing：从人脸与场景中提取情感条件，作为自动情感建议来源。
- LLM-Flow-Dubber：现有仓库主要是演示网页，没有可验证模型接口，列为 Planned。

### 3. Style Director

保持角色在局部音素、词语、句子和更长上下文上的说话风格。

- StyleDubber：核心来源，计划在 `v0.2.0` 接入。
- 产品呈现为“风格参考”和“风格强度”，不暴露论文内部张量或训练配置。

### 4. Character Voice

使用经授权的参考音频保持角色音色，并记录说话人相似度。

- EmoDubber、StyleDubber 和 HPMDubbing 中的说话人建模能力通过统一 `VoiceReference` 接口使用。
- 首版不提供声音库交易、公开声音检索或未经授权的名人声音模板。

### 5. Acoustic Renderer

将 mel-spectrogram 或模型声学输出转换为可播放波形。

- HPMDubbing_Vocoder：提供 16kHz 与 22050Hz HiFi-GAN 路径，作为独立 VocoderAdapter。
- 各模型自带声码器保留为可选适配器，不能将采样率和 hop length 不匹配的模型强行组合。

### 6. Media Composer

负责 FFmpeg 探测、代理文件、音频抽取、片段切分、响度标准化、配音轨拼接和视频混流。该能力由 OpenDub 原生实现，不依赖论文仓库。

### 7. Quality Lab

统一计算和展示：

- 内容：WER/CER 或 ASR 一致性；
- 音色：speaker embedding cosine similarity；
- 情感：分类一致性或 valence/arousal 偏差；
- 同步：目标时长偏差、可用时口型同步指标；
- 音频：响度、削波、静音比例和基础质量检查。

## 仓库归类

| 现有仓库 | OpenDub 角色 | 首次目标版本 | 初始成熟度 | 进入 Stable 的条件 |
|---|---|---:|---|---|
| `EmoDubber` | Emotion Director + Character Voice | `v0.1.0` | Experimental | 真实权重可下载、授权明确、端到端推理通过、情感控制非占位 |
| `HPMDubbing` | Visual Sync Engine + 自动情感条件 | `v0.2.0` | Experimental | 视频预处理可自动化、推理路径无硬编码、样例可复现 |
| `StyleDubber` | Style Director | `v0.2.0` | Experimental | 风格参考输入契约明确、权重可复现、指标与限制齐全 |
| `HPMDubbing_Vocoder` | Acoustic Renderer | `v0.1.0` | Experimental | 权重校验、采样率契约、mel 参数校验和真实音频测试通过 |
| `HD-Dub` / `HDCode` | Visual Sync Engine 候选后端 | `v0.3.0` | Planned | 上游许可、代码、权重、依赖和论文状态全部核验 |
| `CoSyncDiT` | 高级同步扩散后端 | `v0.3.0+` | Planned | 代码和权重正式发布后再设计适配 |
| `LLM-Flow-Dubber` | 上下文/指令控制候选 | `v0.3.0+` | Planned | 从演示页升级为可运行、可许可、可引用的模型资产 |
| `EmoDub` | EmoDubber 演示素材来源 | 不作为适配器 | Reference | 合法示例可迁移，保留来源和授权说明 |
| `HPMDubbing-how-to-get-face-and-lip-` | Vision preprocessing 参考 | `v0.2.0` | Reference | 将流程重写为可测试组件，不能直接依赖手工步骤 |
| `More-Details-about-the-V2C-Animation-dataset.` | 数据与挑战说明 | 文档 | Reference | 仅用于说明和引用，不自动分发版权数据 |
| `V2C_24KHz` | 数据/音频参考 | 后续评估 | Reference | 许可与用途核验后决定是否纳入 |

`LS-GAN` 与视频配音主线无关，不进入 OpenDub 能力图。

## 适配优先级

### 第一优先级：真实可用闭环

1. EmoDubberAdapter
2. HPMVocoderAdapter，或 EmoDubber 官方推理所需的原生声码器适配
3. OpenDub 原生 Media Composer
4. 基础 Quality Lab

### 第二优先级：体现视频配音特色

1. HPMDubbingAdapter
2. 自动口型、人脸和场景特征流水线
3. StyleDubberAdapter
4. 同一片段的模型比较

### 第三优先级：研究预览

1. HD-Dub/HDCode
2. CoSyncDiT
3. LLM-Flow-Dubber

## 能力声明

每个适配器必须显式声明：

```text
languages
requires_video
requires_face
requires_lip_roi
requires_reference_audio
supports_emotion_labels
supports_emotion_strength
supports_valence_arousal
supports_style_reference
supports_duration_control
output_type
sample_rate
minimum_vram_gb
license
weights_license
runtime_isolation
```

UI 根据能力声明展示或禁用控件。任何适配器不得接受一个参数却在内部忽略它。

## 产品命名规则

界面使用能力名作为一级名称，模型名作为二级技术信息：

- “情感导演 / EmoDubber”
- “视觉同步 / HPMDubbing”
- “风格导演 / StyleDubber”
- “波形渲染 / HPM HiFi-GAN”

这使项目既能体现系列研究成果，又不会让用户面对论文仓库结构。
