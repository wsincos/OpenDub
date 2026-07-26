# Product and Experience Design

## 设计主题

OpenDub 的视觉主题是：

> **Editorial Research Instrument，具有电影后期质感的交互式研究仪器。**

它不采用常见 AI 营销站的渐变 Hero、玻璃卡片和发光球体，也不采用普通后台管理系统的表格首页。主视觉来自真实的视频帧、口型区域、音素、韵律曲线、频谱和波形。

“高级感”来自时间同步、信息精度、动画因果关系和内容证据，而不是装饰。

## 品牌

- 品牌：`OpenDub`
- 中文全称：`OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台`
- 英文名称：`OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing`
- 产品描述：`Interactive Method Atlas, Visual Comparison, and Complete-Method Workbench`
- 核心英文句：`See how a scene becomes a voice.`
- 核心中文句：`看见画面如何成为声音。`

品牌文案使用短句、具体名词和可验证动词。避免“颠覆、革命性、全球领先、完美生成、一键最佳”。

Atlas 是平台的首要使用入口：用户在这里理解任务、选择完整方法、查看输入要求和证据状态，并将选择带入 Studio 的本地授权项目。它不是只为申报视频准备的展示页。

## 色彩系统

色彩用于区分模态和状态，不以单一色调覆盖全站：

| Token | 色值 | 语义 |
|---|---:|---|
| `ink-950` | `#111315` | 主文字、深色时间轴 |
| `canvas` | `#F3F5F6` | 全局浅背景 |
| `surface` | `#FFFFFF` | 检查器和浮层 |
| `video` | `#1877C9` | 视频、Scene、Face、Lip |
| `text` | `#7656C1` | 文本和音素 |
| `voice` | `#12836F` | 参考声音、说话人 |
| `prosody` | `#D47A22` | duration、F0、energy |
| `emotion` | `#C84B61` | 情感、valence、arousal |
| `output` | `#2D8A4E` | 生成结果和通过状态 |
| `warning` | `#B77913` | 证据不足和待检查 |
| `error` | `#C43D3D` | 阻断错误 |
| `border` | `#D7DDE0` | 分隔线 |

模态颜色只标记关键轨道、节点边缘和游标状态。背景保持中性，避免页面成为蓝色或紫色单调界面。

## 字体与排版

- 中文：`Noto Sans SC` 或 `Source Han Sans SC`。
- 拉丁与数字：`Inter`。
- 公式、时间码和张量尺寸：`JetBrains Mono`。
- 页面主标题：28 至 36px。
- 方法页标题：24 至 30px。
- 面板标题：15 至 17px。
- 正文：14 至 16px。
- 数据标签：12 至 13px。
- 字距固定为 `0`，不随视口缩放字号。

## 空间与形状

- 基础间距单位：4px。
- 常用间距：8、12、16、24、32、48px。
- 卡片圆角不超过 8px。
- 图谱组件节点圆角 6px。
- 图表、时间轴和视频预览具有稳定高度和 aspect ratio。
- 页面 section 不做漂浮卡片，使用全宽带和清晰分隔。
- 不允许卡片嵌套卡片。

## 动效语言

动画只解释数据关系：

- 输入进入方法时使用 240 至 360ms 的路径推进。
- 点击组件时，高亮边在 180ms 内完成，其他节点降低到 35% 不透明度。
- 时间游标移动使用直接位置更新，不使用弹簧回弹。
- 切换方法保持输入、输出和时间轴位置稳定。
- 频谱、波形不做无数据依据的循环跳动。
- 自动导览总长不超过 45 秒。
- `prefers-reduced-motion` 下取消路径运动和视差，只保留状态切换。

## 图标和控件

- 使用 Lucide 图标。
- 播放、暂停、重置、缩放、固定、下载、引用使用图标按钮并提供 tooltip。
- `Concept / Replay / Live / Planned` 使用带图标的状态标签。
- 视图模式使用 segmented control。
- 时间和强度使用 slider 加数值输入。
- 二元选项使用 switch 或 checkbox。
- 方法选择使用带会议、年份和状态的 searchable select。
- 不使用圆角文本块代替常用播放、缩放、关闭等符号。

## Task Explorer 视觉结构

### 输入区

Video、Text、Reference Speech 三条输入轨具有独立模态颜色和图形语言：

- Video：真实画面，叠加可开关的 Face/Lip 边框。
- Text：自然语言行和音素 token 行。
- Reference Speech：波形和可选择的参考区间。

### 方法区

中心区域不画抽象 AI 大脑。显示当前完整方法名称、四至六个关键步骤和真实进度。未选择方法时使用中性的 `Dubbing Method`。

### 输出区

同时提供 Generated Speech 和 Dubbed Video 两个标签页。主播放区不叠加大段说明文字。

### 时间轴

时间轴跨越输入、方法信号和输出，是第一视口必须出现的元素。游标线从视频帧贯穿到输出波形。

## Method Canvas 视觉结构

- 图谱占据主画布，不放在装饰卡片中。
- 左侧为方法章节和层级导航。
- 右侧为所选组件检查器。
- 下方为可固定的多轨信号台。
- 使用缩放、适配视图、返回上级和重置图标按钮。
- 节点显示组件简称和完整名称，长名称允许换行。
- 边表示论文真实的数据依赖，不能为视觉均衡添加不存在的连接。

## Comparison Lab 视觉结构

- 顶部为单个共享视频和输入摘要。
- 中部为三条等高候选轨。
- 每条轨包含互斥播放、波形、频谱缩略图、状态和指标。
- 盲听模式用 Candidate A/B/C 替代方法名。
- 指标采用紧凑表格或并排刻度，不使用大号仪表盘。
- 用户选择只表示此案例偏好，不生成全局排名。

## 文案示例

推荐：

- `Lip motion constrains duration`
- `Facial expression informs pitch and energy`
- `Reference speech provides speaker identity`
- `Replay from an authorized result bundle`
- `Live model unavailable: checkpoint terms are not verified`

禁止：

- `AI understands everything`
- `Perfect lip sync`
- `Best dubbing model`
- `Real-time`，除非性能测试已经证明
- `Live`，如果实际播放的是预录文件

## 可访问性

- 键盘可完成方法选择、组件选择、播放、时间移动和信号固定。
- 图谱节点使用真实 button/ARIA 语义，而不是只有 pointer 的 `div`。
- 颜色之外同时使用图标、文字和线型。
- 对比度满足 WCAG AA。
- 所有视频包含字幕或文本稿。
- 所有波形和图形信号提供文本摘要。
- 焦点不可被图谱缩放或浮层吞掉。

## 视觉 QA 视口

实现完成前必须用 Playwright 截图检查：

- `1440 x 900`：申报录屏主视口。
- `1920 x 1080`：正式演示影片。
- `1280 x 720`：普通笔记本。
- `768 x 1024`：平板。
- `390 x 844`：移动端。

必须检查文字溢出、图谱遮挡、时间轴错位、空白画布、视频裁切和状态标签真实性。
