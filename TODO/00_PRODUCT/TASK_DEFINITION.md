# Video Dubbing Task Definition

## 标准定义

视频配音生成，也称 Movie Dubbing 或 Visual Voice Cloning，给定静音视频、目标文本和参考语音，生成与视频内容及时间相匹配、同时保持参考说话人身份的目标语音。

```text
Inputs
  V: silent target video
  X: target text or subtitle
  A_ref: authorized reference speech
  C: optional method-specific control

Research method
  A_hat = F_theta(V, X, A_ref, C)

Product rendering
  Y = Mux(V, A_hat)
```

### 输入语义

| 输入 | 必需性 | 提供的信息 | 首屏可视化 |
|---|---|---|---|
| `V` 静音目标视频 | 三套方法必需 | 唇部运动、面部表情、场景上下文、目标时间窗 | 场景画面、Face ROI、Lip ROI、帧游标 |
| `X` 台词或字幕 | 三套方法必需 | 语言内容、音素序列、发音目标 | 文本、音素 token、音素时间片 |
| `A_ref` 授权参考语音 | 三套方法必需 | 目标说话人身份及方法定义的参考风格 | 波形、参考片段范围、授权状态 |
| `C` 方法特定控制 | 可选 | 例如 EmoDubber 的情感类型和强度 | 控件仅在方法支持时显示 |

### 输出语义

- 论文方法直接输出目标配音语音 `A_hat`，可能先生成 mel-spectrogram 再经声码器生成波形。
- OpenDub 将 `A_hat` 与原视频按时间窗混流，输出可播放的配音视频 `Y`。
- UI 必须分别显示“Generated Speech”和“Dubbed Video”，不能将二者混为同一个模型输出。

## 视频配音的四个核心约束

### 内容正确

生成语音应清楚表达输入文本。可观察信号包括音素序列、mel-spectrogram 和 ASR 类指标。

### 时间与口型同步

语音时长、停顿和音素节奏应与视频中的唇部运动相匹配。可观察信号包括 Lip ROI、音素时长、目标时间窗和同步指标。

### 角色身份一致

生成语音应保持授权参考语音中的说话人身份。可观察信号包括参考波形、说话人嵌入相似度和盲听对比。嵌入本身只在明确来源时展示。

### 风格与情感一致

生成语音应表达画面中的局部表情和全局场景氛围。EmoDubber 还允许用户显式指定情感类型和强度。

## 首屏交互叙事

Task Explorer 使用同一段 8 至 12 秒授权视频，按六个状态展开：

1. **Scene**：只播放静音视频，提问“画面如何限制声音？”
2. **Text**：台词进入时间轴并拆分为音素，建立“说什么”的约束。
3. **Voice**：参考语音波形进入，建立“由谁说”的约束。
4. **Visual cues**：点击 Scene、Face、Lip，观察“何时说、怎样说”的视觉线索。
5. **Method**：选择 HPMDubbing、StyleDubber 或 EmoDubber，显示完整方法的处理路径。
6. **Output**：播放目标配音语音，再切换配音视频，完成研究输出到产品输出的闭环。

每个状态都保留前一状态，用户可以前进、后退、直接点击或拖动时间轴。自动演示模式只帮助首访用户理解，任何时候均可接管。

## 首屏数学表达

默认只显示易读形式：

```text
Video + Text + Reference Voice -> Dubbing Method -> Target Speech
```

点击“Formal view”后显示：

```text
A_hat = F_theta(V, X, A_ref, C)
Y = Mux(V, A_hat)
```

数学符号必须带 tooltip，不要求用户先理解公式才能操作。

## 禁止的任务表述

- 不使用 `Video -> Speech`，因为它遗漏了文本和参考语音。
- 不使用 `Text -> Video`，因为项目不生成人物画面。
- 不将参考音频称为 Ground Truth。
- 不将原视频音轨默认作为可公开训练或比较素材。
- 不把 UI 支持的情感控件描述为所有方法都具备的模型能力。
- 不把产品混流得到的视频写成论文模型直接生成的视频。

## 论文依据

- HPMDubbing, CVPR 2023: `https://openaccess.thecvf.com/content/CVPR2023/html/Cong_Learning_To_Dub_Movies_via_Hierarchical_Prosody_Models_CVPR_2023_paper.html`
- StyleDubber, Findings of ACL 2024: `https://aclanthology.org/2024.findings-acl.404/`
- EmoDubber, CVPR 2025: `https://openaccess.thecvf.com/content/CVPR2025/html/Cong_EmoDubber_Towards_High_Quality_and_Emotion_Controllable_Movie_Dubbing_CVPR_2025_paper.html`

正式实现时，界面术语、组件名称和输入输出关系必须从这些原始论文复核，不以二手博客为事实来源。
