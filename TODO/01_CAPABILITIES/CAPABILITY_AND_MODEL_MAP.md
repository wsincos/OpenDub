# Capability and Complete-Method Map

## 基本原则

OpenDub 中的“能力”用于帮助用户理解和筛选完整方法，不用于将不同方法的内部组件重新拼装。

允许：

```text
User need -> filter complete methods -> run or replay one complete method
```

禁止：

```text
HPMDubbing lip module
  + StyleDubber style module
  + EmoDubber emotion module
  -> an unvalidated hybrid model
```

## 一级对象

### Complete Dubbing Method

可独立描述输入、输出、架构和论文结果的视频配音方法。首版只有：

- `galaxycong/hpmdubbing`
- `galaxycong/styledubber`
- `galaxycong/emodubber`

### Supporting Infrastructure

服务于完整方法但不能独立完成 Video + Text + Reference Speech 到目标配音的资产：

- `HPMDubbing_Vocoder`
- 人脸和口型预处理仓库
- 数据转换脚本
- 指标与媒体工具

### Reference / Planned

只有论文、静态 Demo、相关研究或尚未达到接入门槛的仓库。它们可以出现在 Evidence Room 和路线图，不出现在核心三方法选择器。

## 能力筛选维度

| 能力维度 | 用户问题 | HPMDubbing | StyleDubber | EmoDubber |
|---|---|---:|---:|---:|
| Video awareness | 是否使用视频信息 | 是 | 是 | 是 |
| Lip-duration sync | 是否显式建模口型和时长 | 是 | 是 | 是 |
| Facial prosody | 是否从面部表情获得韵律或情感线索 | 是 | 是 | 是 |
| Scene context | 是否显式使用全局场景情感 | 是 | 以论文实际实现为准 | 以论文实际实现为准 |
| Reference identity | 是否使用参考语音保持说话人 | 是 | 是 | 是 |
| Phoneme-level modeling | 是否突出音素级建模 | 部分 | 核心 | 核心 |
| Multi-scale style | 是否突出音素级和话语级风格 | 否 | 核心 | 否 |
| User emotion category | 是否接受用户指定情感 | 否 | 否 | 是 |
| User emotion intensity | 是否接受用户指定强度 | 否 | 否 | 是 |
| Direct waveform generation | 方法主干是否直接生成波形 | 否 | 否 | 是，按论文 FUEC 描述 |

表格中的“否”表示该方法没有将其作为明确的用户能力或核心贡献，不表示模型输出完全不存在相关属性。

## 需求到方法的选择逻辑

OpenDub 可以提供规则化筛选，但不能给出无条件全局排名：

| 首要需求 | 推荐查看 | 推荐理由的表达边界 |
|---|---|---|
| 理解视频的 Lip、Face、Scene 如何影响韵律 | HPMDubbing | 论文将三层视觉信息分别关联到 duration、pitch/energy 和 global emotion |
| 观察音素级与话语级风格学习 | StyleDubber | 论文以 MPA、PLA、USL 处理发音、对齐和整体风格 |
| 用户指定情感类型和强度 | EmoDubber | 三套方法中只有 EmoDubber 将此定义为显式用户控制 |
| 比较不同研究演进 | 三套方法 | 使用同案例 Replay 或共同支持的 Live 输入 |

UI 文案应使用“适合查看”“支持该控制”“本案例指标更高/更低”，不使用“绝对最佳”。

## 状态与可用性

方法的运行状态与内容状态分别记录：

### 运行状态

- `unavailable`：没有满足许可与运行门槛的适配器。
- `experimental`：真实运行成功，但环境或输入限制较强。
- `stable`：通过发布门槛和真实回归测试。

### 内容状态

- `concept`：有论文依据的交互解释。
- `replay`：有授权结果包。
- `live`：可运行且可导出信号。
- `planned`：尚无足够内容。

一个方法可以同时是 `runtime=unavailable` 和 `content=concept,replay`。页面不得因为没有 Live 而隐藏已经可信的 Concept 或 Replay。

## 首版准入表

| 方法 | Concept | Replay | Live | 首版动作 |
|---|---:|---:|---:|---|
| HPMDubbing | 必须 | 至少争取一个 | 条件项 | 完成完整 Method Canvas |
| StyleDubber | 必须 | 至少争取一个 | 条件项 | 完成完整 Method Canvas |
| EmoDubber | 必须 | 至少争取一个 | 第一优先条件项 | 完成完整 Method Canvas 和情感控制解释 |
| HPMDubbing_Vocoder | Supporting | 可作为信号阶段 | 条件项 | 只在方法输出阶段和 Evidence Room 出现 |
| LLM-Flow-Dubber | Planned | 不承诺 | 不承诺 | 路线图或相关成果 |
| HDCode | Reference | 不承诺 | 不承诺 | Evidence Room |
| CoSyncDiT | Planned | 不承诺 | 不承诺 | 路线图 |

## 完整方法接入门槛

一个第三方或团队后续方法只有满足以下条件才能加入核心 Method Atlas：

1. 有明确论文或技术报告。
2. 有稳定方法 ID、输入和输出定义。
3. 能作为完整方法独立运行，或有合法 Replay Bundle。
4. 有至少四个可解释组件和对应来源。
5. 代码、权重、素材和结果许可分别记录。
6. 支持统一时间轴或能提供明确的静态非时序解释。
7. 不要求 OpenDub 与另一方法内部组件拼接才能成立。
