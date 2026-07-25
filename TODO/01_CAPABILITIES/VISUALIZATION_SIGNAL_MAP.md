# Visualization Signal Map

## 目的

OpenDub 借鉴 CNN Explainer 和 Distill 一类交互解释的优点，但展示对象不是卷积核，而是沿同一时间轴关联的视频、文本、韵律、频谱和语音。

每个可视信号都必须回答一个具体问题：

- 它来自哪里？
- 它在方法中影响什么？
- 它是 Concept、Replay 还是 Live？
- 它能否与时间游标同步？

## 信号类型

| Signal Type | 数据形式 | 推荐渲染器 | 是否时序 |
|---|---|---|---:|
| `video.scene` | MP4/WebM 或帧索引 | video player + frame strip | 是 |
| `video.face_roi` | 图像序列或 bounding boxes | canvas overlay + thumbnails | 是 |
| `video.lip_roi` | 图像序列或 bounding boxes | ROI strip | 是 |
| `text.transcript` | 字符串与时间范围 | subtitle track | 是 |
| `text.phonemes` | token + start/end | token timeline | 是 |
| `audio.reference` | WAV/FLAC | waveform | 是 |
| `audio.generated` | WAV/FLAC | waveform | 是 |
| `acoustic.mel` | matrix + axes | WebGL/canvas spectrogram | 是 |
| `prosody.duration` | token durations | aligned bars | 是 |
| `prosody.f0` | Hz array + hop | line plot | 是 |
| `prosody.energy` | normalized or physical units | area/line plot | 是 |
| `emotion.valence_arousal` | 2D points or path | VA plane | 可选 |
| `emotion.category` | label + score | compact categorical track | 可选 |
| `alignment.matrix` | source x target matrix | heatmap | 是 |
| `embedding.projection` | 2D projection + method | scatter plot | 否 |
| `flow.trajectory` | steps x dimensions/projection | trajectory plot | 可选 |
| `metric.scalar` | value + unit + direction | value/compact scale | 否 |

## 来源等级

每个信号 manifest 必须包含 `provenance.mode`：

### `concept`

- 从论文事实转译的结构、标签和关系。
- 可以使用示意曲线，但必须 `illustrative=true`。
- 不允许把示意值用于指标或方法比较。

### `replay`

- 来自一次历史或预计算运行。
- 包含 source commit、weights hash、参数、案例来源和文件 hash。
- 允许时间同步、播放和比较。

### `live`

- 来自当前 OpenDub run。
- 由 Adapter 或 VisualizationProvider 写入。
- run manifest 与信号文件原子完成后才对 UI 可见。

## 统一时间基准

- 时间统一为整数微秒 `time_us`。
- 等间隔数组使用 `start_us`、`hop_us` 和 `values`。
- token 使用 `start_us`、`end_us`。
- 视频帧使用真实 PTS，不使用假定恒定 FPS 的数组下标。
- 音频波形使用 sample index，UI 通过 sample rate 转换。
- 方法内部张量如果不能映射到时间，不得强行与播放游标同步。

## 渲染规则

### 波形

- 原始波形与归一化显示分开。
- 方法比较应用同一 LUFS 播放规范，但保留原始文件下载。
- 缩放级别稳定，不因候选峰值自动改变纵轴后造成错误感知。

### Mel-spectrogram

- 标明采样率、hop length、mel bins 和色阶范围。
- 比较模式使用相同频率范围和色阶。
- 不把 JPEG 截图作为 Live 信号格式。

### F0 与 Energy

- 无声区使用空值，不用零值连接。
- F0 以 Hz 或半音明确标注。
- Energy 必须说明归一化方式，不能跨不同归一化方法比较绝对值。

### Alignment

- 横纵轴必须是明确的 token、frame 或 time。
- hover 同时突出源和目标。
- 超大矩阵按层级或 tile 渲染，不能冻结主线程。

### Embedding

- 只有明确导出点和投影算法时才展示。
- 标明 PCA、t-SNE 或 UMAP 及随机种子。
- 2D 距离不直接声称等于语义相似度。

## 三方法最小信号集

### HPMDubbing

- 必须：Scene frames、Face ROI、Lip ROI、phonemes、duration、F0、energy、mel、generated waveform。
- 可选：valence/arousal、scene emotion、attention。
- 禁止：没有导出来源的“层间激活”动画。

### StyleDubber

- 必须：video frames、Lip ROI、phonemes、reference waveform、phoneme alignment、mel、generated waveform。
- 可选：MPA attention、utterance style representation、pre/post mel。
- 禁止：将普通音量包络标记为 style embedding。

### EmoDubber

- 必须：Lip ROI、phonemes、reference waveform、emotion label/intensity、generated waveform。
- Replay 启用 PE 细节时：video-level phoneme expansion、alignment path。
- Live 可选：acoustic prior projection、flow trajectory、positive/negative guidance scores。
- 禁止：用音量放大模拟情感强度。

## 信号降级

当信号缺失时：

1. 保留组件节点。
2. 显示论文依据的 Concept 解释。
3. 检查器明确写 `No replay/live signal available`。
4. 不用随机数、CSS 波浪或复制其他方法的数据填充。
5. 比较指标标记 `unavailable` 或 `not_applicable`。

## 性能预算

- 单个 Replay Bundle 的首屏元数据小于 200KB。
- 单个时间序列 JSON 小于 2MB；更大数据使用二进制数组。
- 视频提供 720p 演示代理，原始文件不随首页加载。
- 波形峰值预计算为多分辨率层级。
- 图谱首次渲染小于 100ms。
- 频谱和 heatmap 使用 Canvas/WebGL，不创建数万个 DOM 元素。

## 内容制作检查表

- [ ] 信号名称与论文术语一致。
- [ ] 数据单位和范围明确。
- [ ] 时间基准明确。
- [ ] 来源模式明确。
- [ ] 文件 hash 完整。
- [ ] 素材与声音允许公开展示。
- [ ] Concept 示例已标记 illustrative。
- [ ] Replay/Live 可以追溯到 run manifest。
- [ ] 相同指标具有相同预处理。
- [ ] 组件缺失信号时降级文案准确。
