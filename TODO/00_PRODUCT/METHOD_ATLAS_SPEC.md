# OpenDub Method Atlas Product Specification

## 产品结构

OpenDub 使用一个连续但可深链接的交互体验：

| 路由 | 名称 | 主要任务 |
|---|---|---|
| `/explore` | Task Explorer | 理解视频配音输入、约束和输出 |
| `/methods` | Method Atlas | 浏览三套完整方法及其差异 |
| `/methods/:methodId` | Method Canvas | 逐组件理解一套方法 |
| `/compare/:caseId` | Comparison Lab | 同一输入下比较多个结果 |
| `/studio` | OpenDub Studio | 管理素材、运行 Live 方法并导出 |
| `/evidence` | Evidence Room | 查看论文、代码、权重、许可与运行证据 |

默认入口是 `/explore`。项目列表和时间线工作台不再是第一次访问时的首屏。

## 全局应用框架

### 顶部导航

- 左侧：OpenDub 标志和当前空间名称。
- 中部：`Explore`、`Methods`、`Compare`、`Studio`。
- 右侧：状态图例、语言切换、GitHub、无障碍动画开关。
- 移动端：保留品牌、当前视图和菜单图标，不压缩成无法阅读的文本按钮。

### 全局时间游标

所有包含时序数据的视图共享 `currentTimeUs`：

- 视频帧。
- Lip ROI 与 Face ROI。
- 文本和音素。
- F0、energy、duration。
- mel-spectrogram。
- 波形和播放头。

任一视图拖动游标时，其他视图在一个动画帧内同步。时间游标是产品的核心交互，不是装饰。

## Task Explorer

### 桌面布局

使用三列固定关系而非浮动卡片堆叠：

```text
Inputs                 Method                    Output
Video                  selected method           Generated Speech
Text                   state + data flow          Dubbed Video
Reference Speech
Optional Control
```

底部是跨全宽的同步时间轴。首屏高度应让用户看到时间轴和下一部分标题，避免将内容藏在超高 Hero 内。

### 输入检查器

- 点击 `Video`：展开 Scene、Face、Lip 三层。
- 点击 `Text`：在自然语言和音素序列之间切换。
- 点击 `Reference Speech`：显示授权标签、波形和选中范围。
- 点击可选控制：只显示当前方法声明支持的控制。

### 输出检查器

- `Speech`：试听、波形、频谱、时长。
- `Dubbed Video`：画面与生成语音组合后的产品输出。
- `A/B`：在静音、参考、生成结果之间切换，不允许同时重叠播放。

### 自动导览

首次访问自动播放 35 至 45 秒的六阶段导览。用户首次点击、按键或拖动后立即停止自动推进。`prefers-reduced-motion` 下使用淡入和高亮替代飞线与轨迹动画。

## Method Atlas

### 组织原则

方法不是功能卡片，也不是可互换的内部组件。Atlas 以“研究问题如何演进”为组织线：

1. HPMDubbing：从视觉层级建立韵律。
2. StyleDubber：从帧级转向音素级的多尺度风格学习。
3. EmoDubber：在同步和清晰度基础上加入用户可控情感。

每个方法入口显示：

- 论文名称、会议和年份。
- 一句话研究问题。
- 完整输入和输出。
- 关键组件名称。
- 当前展示状态。
- 可用案例数量。
- Source、Paper、Cite 三个明确动作。

### Method Canvas

Method Canvas 使用有向图，但不绘制无意义的神经网络层。

组件节点支持四种动作：

- `Select`：高亮进入和离开该节点的边。
- `Inspect`：打开信号检查器。
- `Pin`：将组件信号固定在下方时间轨。
- `Compare`：在有消融或多方法对应信号时进入比较视图。

信号检查器必须包含：

- 该组件解决的问题。
- 输入与输出的数据类型。
- 与时间游标同步的实际或策划信号。
- 来源模式：Concept、Replay 或 Live。
- 论文章节和代码入口。
- 不能从现有证据推出的内容。

### Method Canvas 层级

1. `Overview`：8 秒内理解方法的主路径。
2. `Flow`：点击组件和边。
3. `Signals`：固定多个时间对齐轨道。
4. `Evidence`：论文图表、消融、音频结果和引用。
5. `Reproduce`：环境、权重、输入、命令和状态。

## Comparison Lab

Comparison Lab 不输出“绝对最好模型”，而是帮助用户根据需求选择。

### 比较输入

- 一个固定 `caseId`。
- 同一视频裁剪。
- 同一文本。
- 同一授权参考语音。
- 各方法真实支持的控制参数。

### 比较视图

- 视频只显示一次，避免视觉重复。
- 结果使用三条横向音轨。
- 播放按钮为互斥播放。
- 支持瞬时 A/B/C 切换并保持相同时间位置。
- 共同指标横向对齐。
- 不适用指标显示 `N/A` 及原因。
- 支持盲听模式，隐藏方法名直至用户提交偏好。

### 选择建议

只允许基于可见证据生成场景化提示，例如：

- “此案例中，候选 B 的时长偏差更低。”
- “候选 C 提供用户情感强度控制。”

禁止显示“OpenDub AI 自动选择全局最佳模型”之类无法验证的结论。

## Studio 与公开 Atlas 的关系

Atlas 是公开、无需 GPU 的主要体验。Studio 是本地创作和 Live 运行空间：

- Atlas 可独立使用 Concept 和 Replay 内容。
- Studio 负责导入素材、授权、生成、评测和导出。
- Live 结果生成后可以被打包成私有或可分发 Replay Bundle。
- 一个 Live 运行失败不能破坏 Atlas 的教学和申报演示。

## 内容状态

| 状态 | 含义 | 是否需要 checkpoint | 是否可在申报视频中展示 |
|---|---|---:|---|
| `Concept` | 依据论文重绘的交互解释 | 否 | 可以，必须显示标签 |
| `Replay` | 授权的历史或预计算结果包 | 否 | 可以，必须记录来源 |
| `Live` | 当前环境真实执行并产生中间产物 | 是 | 可以，必须保留运行证据 |
| `Planned` | 尚未接入或证据不足 | 否 | 只可作为路线图 |

状态标签在方法页标题、案例选择器、播放区和导出报告中保持一致。

## 响应式范围

- `>=1280px`：完整三列 Task Explorer、图谱和多轨比较。
- `768px-1279px`：输入检查器变为可切换侧栏，图谱保持可缩放画布。
- `<768px`：支持 Task Explorer、方法浏览、单轨试听和纵向信号轨；不支持复杂图谱编辑或三轨同时展开。

## 体验验收

首次访问的评审无需阅读 README，应能在三分钟内：

1. 准确说出三项核心输入和研究输出。
2. 说出视频配音区别于普通 TTS 的至少三个约束。
3. 打开任意一套方法并点击至少两个组件。
4. 区分 Concept、Replay 和 Live。
5. 用同一案例比较至少两个方法结果。
6. 找到论文、代码和许可证据。
