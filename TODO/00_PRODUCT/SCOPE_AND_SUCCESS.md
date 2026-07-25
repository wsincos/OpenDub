# Scope and Success Criteria

## 申报版本范围

申报版本目标是一个可公开访问、无需 GPU 即可理解和体验的 Method Atlas。Live 推理是增强项，不是首页成立的前提。

### 必须完成

- Task Explorer 完整解释三输入、研究输出和产品输出。
- HPMDubbing、StyleDubber、EmoDubber 三套完整 Concept Method Canvas。
- 每套方法至少四个可点击组件和三类有语义信号。
- 至少一个授权案例的 Replay Bundle。
- 至少两个方法可进入同输入 Comparison Lab。
- 论文、代码、提交版本、许可证和状态入口。
- 中文主界面和英文术语对照。
- 桌面端、平板和移动端可访问展示。
- 申报主视频、60 秒剪辑和静态截图。

### 条件完成

- 至少一套方法的真实 Live 适配器。
- Live 中间产物实时或运行后导入 Method Canvas。
- 三套方法共同案例的完整对比。

条件项只有在权重许可、SHA-256、运行环境和授权素材全部满足时才升级为承诺项。

### 明确不做

- 不训练新的基础配音模型。
- 不组合三套方法的内部模块。
- 不支持任意第三方视频配音方法。
- 不承诺实时生成。
- 不承诺任意语言。
- 不构建云端账号、计费、协作和模型托管。
- 不复制论文原图作为 UI 主体，架构图应依据论文重新绘制并引用。

## 内容验收

### Task Explorer

- 三项必需输入均可点击并显示准确语义。
- Formal view 公式和自然语言定义一致。
- 输出清楚区分 Speech 与 Dubbed Video。
- 自动导览不超过 45 秒，用户交互立即停止自动播放。
- 拖动时间游标后所有时序视图偏差不超过一个屏幕像素对应的时间量。

### HPMDubbing

- 展示 Lip、Face、Scene 三层视觉来源。
- 展示 duration、pitch/energy 和 global emotion 的关系。
- 展示 mel-spectrogram 到 waveform 的输出阶段。
- 不将 HPMDubbing_Vocoder描述为独立完整方法。

### StyleDubber

- 展示 MPA、PLA、USL 三个论文核心组件。
- 清楚表达从 frame-level 到 phoneme-level 的研究动机。
- 显示参考语音、视觉特征、音素和 utterance-level style 的作用边界。

### EmoDubber

- 展示 LPA、PE、speaker identity adapting、FUEC。
- 情感类别和强度控件仅在该方法内容中激活。
- 正负引导的视觉表达与论文描述一致。
- 发音、同步和情感控制分别有证据入口。

## 工程验收

- 内容 manifest 通过 JSON Schema 校验。
- Replay Bundle 具有资源哈希、时间基准、来源和分发权限。
- Atlas 在断开 API 和 GPU 时仍可完整浏览 Concept/Replay 内容。
- 方法状态由 manifest 驱动，不在组件中硬编码。
- 路由可深链接、刷新和浏览器前进后退。
- Web 单元与组件测试覆盖核心状态。
- Playwright 覆盖 Task Explorer、三个方法页、Compare 和状态标签。
- `pnpm build`、`make check`、链接检查和无障碍扫描通过。

## 申报成功指标

邀请五名未参与项目的 AI 相关用户完成三分钟可用性测试：

- 5/5 能说出 Video、Text、Reference Speech。
- 至少 4/5 能区分研究输出和产品输出。
- 至少 4/5 能说明三套方法各自解决的核心问题。
- 5/5 能找到 Concept/Replay/Live 状态。
- 至少 4/5 能完成一次 A/B 比较。

## 性能目标

- 首次内容绘制在本地生产构建中小于 1.5 秒。
- 首屏关键 JS gzip 后目标小于 250KB，方法页图表按路由懒加载。
- 交互到下一帧反馈小于 100ms。
- 1440x900 下拖动时间游标保持 50 FPS 以上。
- Replay 音视频切换不重新下载已经缓存的资源。

## 真实性门槛

### Concept

- 每个组件有论文章节引用。
- 每条边有输入输出语义。
- 模拟曲线显式标记 `Illustrative`。

### Replay

- 资源有 SHA-256。
- 记录生成来源、方法版本和是否允许分发。
- 未知来源媒体不得加入公开包。

### Live

- 源码提交固定。
- 权重许可明确并记录 SHA-256。
- 输入、参数、环境和输出保存在 run manifest。
- 真实烟雾测试通过。
- 页面不能用 Replay 数据替代失败的 Live 运行。

## 发布门槛

以下条件全部满足才能发布 `v0.1.0-atlas`：

1. 三套 Concept Canvas 经过论文作者或项目负责人核验。
2. 至少一个公开 Replay Bundle 通过素材和声音权利审计。
3. 全部自动化测试和视觉 QA 通过。
4. README、快速开始、引用、许可证和已知限制齐全。
5. 申报视频中的每个功能均能在发布版本复现。
