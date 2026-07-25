# Master Script

本文是 2 分 40 秒正式版母版。方括号是画面/状态提示，不朗读。每句旁白在最终录制前必须通过 [TRUTH_AND_QA.md](TRUTH_AND_QA.md)。

## 00:00-00:09 | 冷开场

**画面**：同一授权人物近景回到相同起点两次。第一遍播放参考的平直朗读，第二遍播放该案例的 Replay 或 Live 目标配音。左上角清楚标记两段来源与模式。

**现场声音**：两段声音各 3 秒，中间 300ms 静音，无音乐。

**屏幕文字**：`同一句台词。画面决定它该怎样被说出。`

**旁白**：无。

## 00:09-00:24 | 任务定义

**画面**：进入 Task Explorer。Video、Text、Reference Speech 三条输入被依次点击，时间游标同步移动。

**旁白**：

> 视频配音不是把一句文字读出来。它要让一段目标语音，同时匹配画面的口型、角色的状态、目标台词和参考声音。

**屏幕文字**：`Video + Text + Reference Speech -> Target Speech`

## 00:24-00:34 | 研究输出与产品输出

**画面**：Task Explorer 切换 Generated Speech 和 Dubbed Video 标签。前者显示波形和频谱，后者显示回填到视频后的成片。

**旁白**：

> 模型生成的是目标语音。OpenDub 再把它回填到视频，形成可以审听和导出的配音成片。

## 00:34-00:56 | HPMDubbing

**画面**：点击 HPMDubbing。Method Canvas 依次选择 Lip Motion、Face Affect、Scene Emotion。下方固定 duration、F0、energy 和 mel 信号。

**旁白**：

> HPMDubbing 从三个层级理解画面。口型约束时长，面部表情影响音高和能量，场景提供全局情感线索。

**屏幕文字**：`Lip -> Duration  |  Face -> Pitch / Energy  |  Scene -> Emotion`

## 00:56-01:17 | StyleDubber

**画面**：切换 StyleDubber。frame view 和 phoneme view 来回切换，再选中 MPA、PLA、USL。

**旁白**：

> StyleDubber 把学习重点从逐帧对齐转向音素级表达。它用局部发音风格、口型对齐和整句风格，共同塑造更完整的角色声音。

**屏幕文字**：`Phoneme-level style | Lip alignment | Utterance-level style`

## 01:17-01:38 | EmoDubber

**画面**：切换 EmoDubber。LPA、PE、Speaker Identity 和 FUEC 被依次点亮。情感类别和强度控件显示当前模式标签。

**旁白**：

> EmoDubber 在同步和清晰发音之外，加入用户指定的情感类型与强度。每一项控制都由状态标签说明，它是论文解释、历史回放，还是本机真实运行。

**屏幕文字**：`LPA | Pronunciation Enhancing | Speaker Identity | Emotion Guidance`

## 01:38-02:01 | 比较与选择

**画面 A：通过 Comparison Gate**：Comparison Lab 使用同一案例，互斥播放 Candidate A、B、C，播放位置保持一致，随后显示共同适用指标和盲听结果。

**旁白 A**：

> 当多个方法共享完全相同的输入，OpenDub 才允许将它们放在同一条时间线上比较。播放、指标和版本证据始终对齐，选择依据来自当前案例，而不是一个虚假的全局排名。

**画面 B：未通过 Comparison Gate**：显示 Comparison Gate 页面与方法专属 Replay，不进行 A/B/C 音频优劣切换。

**旁白 B**：

> 不同来源的 Demo 不能被伪装成公平比较。OpenDub 先保留每个方法的真实证据，只有共享相同输入的结果才能进入比较实验室。

## 02:01-02:21 | 证据和开源

**画面**：Evidence Room。依次显示 Paper、Source commit、Code license、Weight status、Content mode、Replay/run evidence。

**旁白**：

> 每个方法都连接到论文、源码、版本、许可和结果证据。Concept、Replay、Live 和 Planned 被明确区分，让开放展示不以夸大为代价。

## 02:21-02:36 | 平台收束

**画面**：从 Evidence Room 拉回 Task Explorer，再回放完整配音视频。右侧短暂出现 GitHub 地址。

**旁白**：

> OpenDub 保留每一种方法的完整性，也把视频配音的理解、比较和复现，变成每个人都能看见和参与的开源体验。

## 02:36-02:40 | 片尾

**画面**：静帧。

```text
OpenDub
看见画面如何成为声音。
github.com/wsincos/OpenDub
```

**旁白**：`OpenDub. See how a scene becomes a voice.`
