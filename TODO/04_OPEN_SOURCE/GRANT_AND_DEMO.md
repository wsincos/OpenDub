# Grant Positioning and Deliverables

## 最终申报方式

一次申报对应一个项目、一个项目名称和一个主仓库：

- 项目名称：`OpenDub`
- 中文全称：`OpenDub 视频配音生成交互式方法图谱与开源平台`
- 主仓库：`https://github.com/wsincos/OpenDub`
- 申报方向：`AIGC 应用与工具`
- 推荐档位：重点级
- 推荐申请金额：12,000 元

HPMDubbing、StyleDubber、EmoDubber 是 OpenDub 的三项核心完整方法和技术基础，不作为三个并列申报项目。

## 一句话摘要

OpenDub 面向视频配音生成任务，建设无需 GPU 即可使用的交互式任务解释器、完整方法图谱和同输入比较平台，并在许可和权重条件满足时提供可复现的本地真实运行。

## 申报摘要

视频配音生成需要同时利用静音视频、目标文本和授权参考语音，生成与角色口型、画面情绪、说话节奏和目标音色一致的语音。现有研究通常以论文、独立代码仓库和静态 Demo 形式发布，任务理解、方法复现、过程观察和结果比较之间仍存在明显断裂。

OpenDub 基于团队在 HPMDubbing、StyleDubber、EmoDubber 等视频配音研究中的连续积累，将三套方法保留为完整、独立的生成方法，并建立统一的任务输入、交互式方法图谱、时间对齐信号、结果回放、同输入比较和复现证据协议。用户可以点击 Lip、Face、Scene、phoneme alignment、style learning、emotion guidance 等组件，观察视频帧、音素、duration、F0、energy、mel-spectrogram 和波形如何沿统一时间轴变化。

项目使用 Concept、Replay、Live、Planned 四级状态区分论文解释、授权历史结果、现场运行和规划能力。即使没有 GPU，用户也能完整理解和探索方法；具备合法 checkpoint 和运行环境后，可通过隔离适配器执行完整方法并将中间产物导入同一可视化界面。

## 为什么不是历史成果打包

团队原有贡献：

- HPMDubbing：Lip、Face、Scene 的分层韵律建模。
- StyleDubber：音素级与话语级多尺度风格学习。
- EmoDubber：同步、发音增强和用户情感类型/强度控制。

OpenDub 新增贡献：

1. 准确、交互式的视频配音任务表达。
2. 完整方法的声明式图谱协议。
3. 视频、文本、韵律、频谱和语音的统一时间轴。
4. Concept/Replay/Live/Planned 真实性规范。
5. 同输入方法比较和指标适用性规范。
6. 从 Live 运行到可审核 Replay Bundle 的开源工具链。
7. 论文、代码、权重、素材权利和运行证据的一体化 Evidence Room。

这些工作形成独立平台价值，不依赖“再训练一个新模型”才能成立。

## 项目特色

### 任务可解释

用户首先理解：

```text
Video + Text + Reference Speech -> Dubbing Method -> Target Speech
```

再进入三套方法，不会把视频配音误解为普通 TTS。

### 方法完整

不跨论文拼接内部组件。OpenDub 统一的是外围输入、观察、比较和复现协议。

### 时间可交互

一个游标同步视频、Lip ROI、Face ROI、phonemes、duration、F0、energy、mel 和 waveform。

### 结果可比较

只有共同输入 hash 一致的结果才能进入 Comparison Lab。缺失和不适用指标不填零、不静默降级。

### 状态可信

预录 Demo 不标 Live，示意曲线不参与指标，权重许可不明确时不自动下载。

## 资助周期交付

### 必交付

- Task Explorer。
- 三套 Concept Method Canvas。
- 三套结构化方法 manifest 和作者核验表。
- 至少一个合法 Replay Bundle。
- Comparison Lab 工具链及相同输入准入规则。
- Evidence Room。
- 中文 README、快速开始、方法文档和贡献规范。
- 2 分 40 秒正式影片、60 秒和 30 秒版本。
- `v0.1.0-atlas` 发布。

### 条件交付

- 至少一个真实 Live Adapter。
- Live 中间产物 VisualizationProvider。
- 至少两个方法在同一授权案例上的公开比较。

条件交付未满足时明确说明外部权重和素材约束，不以虚假实现替代。

## 里程碑

| 里程碑 | 周期 | 交付 |
|---|---|---|
| M1 | 第 1-2 周 | 内容 Schema、路由、Task Explorer |
| M2 | 第 3-5 周 | 三套 Method Canvas、Signal Dock、Evidence |
| M3 | 第 6-7 周 | Replay 工具链、授权内容、Comparison Lab |
| M4 | 第 8 周 | 作者复核、性能与无障碍 QA |
| M5 | 第 9 周 | 影片、文档、发布候选 |
| M6 | 第 10 周 | 公开发布、社区反馈和结项证据 |

Live Adapter 从第 3 周并行审计，只有准入通过后进入公开里程碑。

## 预算建议

| 项目 | 金额 | 用途 |
|---|---:|---|
| 内容与素材制作 | 2,500 元 | 自制授权视频、参考声音、字幕和 Concept 内容 |
| 交互可视化开发 | 3,500 元 | 图谱、信号渲染、时间同步和响应式 QA |
| 模型复现与算力 | 2,500 元 | 合法 checkpoint 验证、GPU 推理、Replay 产出 |
| 文档与开源治理 | 1,000 元 | 中英文文档、Schema、许可和贡献模板 |
| 演示影片与后期 | 2,000 元 | 录制、配音、剪辑、字幕、音频混合 |
| 测试与发布 | 500 元 | 可访问性、浏览器测试和制品托管 |
| 合计 | 12,000 元 | 重点级申请 |

若只能申请基础级 4,000 元，范围缩减为 Task Explorer、三套 Concept Canvas、一个 Replay 和 60 秒影片，不承诺 Live。

## 可量化指标

- 三套方法、至少 18 个核心组件可点击。
- 至少 20 类方法事实和信号通过 Schema 校验。
- 首访用户三分钟任务理解正确率达到 80% 以上。
- 五个目标视口完成自动和人工 QA。
- 公开 Replay 的来源、rights 和 hash 覆盖率 100%。
- 三套方法的核心节点作者复核覆盖率 100%。
- 至少发布一个外部开发者可复制的方法 manifest 模板。

## 风险回答

### 没有 checkpoint 怎么办

Concept 和合法历史 Demo Replay 不需要 checkpoint。只有 Live 和重新生成同输入结果需要 checkpoint。

### 是否只是论文展示网页

不是。OpenDub 同时提供版本化内容契约、时间同步信号、Replay 打包工具、比较准入、运行追踪和可选 Live 适配。

### 是否把不同模型混合成一个新模型

不是。三套方法保持完整，能力维度只用于筛选和解释。

### 如何避免夸大

所有界面和影片强制显示 Concept、Replay、Live、Planned；状态由证据推导。

## 申报视频

正式导演脚本和录制流程见 [DEMO_FILM/README.md](DEMO_FILM/README.md)。影片的第一主角是“视频配音任务如何发生”，第二主角是三套方法的研究演进，第三主角才是平台工程。
