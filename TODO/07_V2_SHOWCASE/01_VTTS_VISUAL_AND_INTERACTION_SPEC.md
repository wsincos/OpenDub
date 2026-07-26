# V2 VTTS 视觉与交互规格

## 1. 体验定位

页面名称：`VTTS Task Stage`。
路由：`/vtts`。
进入方式：首次在演示路线访问 `/vtts`；导航中以 `Task` 显示；用户可进入 `/explore` 查看完整工作台。

它不是营销落地页。它的每一个镜头都服务于任务理解、案例检查或方法选择，并可通过键盘、触控和 reduced-motion 使用。

## 2. 首屏构图

采用横向“电影输入 -> 约束汇聚 -> 输出媒体”的单一画幅，不再使用三列卡片。

```text
  [Silent video filmstrip] ---- visual timing packets ----\
                                                        [Complete method] ----> [Target speech waveform]
  [Target text + IPA] -------- phoneme timing tokens ----/                         |
                                                                                     +--> [Dubbed video]
  [Authorized reference wave] -- identity/style envelope --/
```

### 左侧：三条有材质的输入轨

- **Silent video**：16:9 画面和 5–7 帧胶片带，胶片孔由 CSS/SVG 绘制；没有使用第三方插图作为装饰。
- **Target text**：一行已核对的台词，下方是等宽 IPA token 与实际时段，不显示凭空生成的拼音或英文单词。
- **Authorized reference speech**：同一参考音频的精简波形，展示授权状态而不显示真实身份信息。

### 中部：完整方法聚合器

- 使用细边框、`Complete method` 标识和可点击步骤，不画“黑色 AI 黑箱”。
- 默认显示“完整方法”，只有用户按需求选择后才显示 HPMDubbing、StyleDubber 或 EmoDubber。
- 输入脉冲在每条真实路径上移动；进入中心时按各自模态色叠加，而不是变为无意义粒子。
- 点击中心打开 `/methods`，不会触发生成请求。

### 右侧：两个可区分输出

- **Target speech**：真实输出音频或授权 GT 的波形、时长和内容状态；无法提供时明确显示 `Task illustration`，不显示假波形。
- **Dubbed video**：由同一案例的画面和对应音频组成的 16:9 回放；只有合格案例才允许播放。

## 3. 动画状态机

| 状态 | 画面 | 时长 | 用户可见意义 |
| --- | --- | ---: | --- |
| `idle` | 静态完整任务图 + 轻微游标呼吸 | 0 秒 | 可自由检查，不暗示运行 |
| `video-cues` | 电影条推进，Face / Lip / Environment 依次点亮 | 1.8 秒 | 视频提供多个时间约束 |
| `text-timing` | IPA token 沿播放头出现 | 1.2 秒 | 台词决定说什么与何时说 |
| `reference-identity` | 参考波形描边推进 | 1.0 秒 | 参考音频提供允许使用的声音特征 |
| `method-resolve` | 三路信号进入完整方法，方法标签亮起 | 1.4 秒 | 一套完整方法共同处理约束 |
| `outputs` | 目标语音波形与配音视频先后出现 | 1.6 秒 | 区分研究输出和产品输出 |
| `paused` | 保持当前帧，所有文字和链接可读 | 无限 | 可审查、可录制 |

自动导览总长不超过 8 秒，默认只播放一次。用户通过播放、暂停、重置图标操作；`prefers-reduced-motion: reduce` 直接呈现 `idle` 终态并保留点击检查。

## 4. 同步线索显微镜

保留并重做 V1 的 `One scene carries several timing cues`，标题改为：

> **One scene constrains more than lip timing.**
> 一段画面同时约束口型、表情与环境节奏。

四个检查层：

| 层 | 视觉呈现 | 解释 |
| --- | --- | --- |
| Face | 人脸框 / 表情强度轨 | 面部情感可影响能量、音高和整体表达 |
| Lip | 嘴部 ROI / 开合时间轨 | 口型对齐约束局部时长和发音节奏 |
| Environment | 场景裁切、镜头变换或运动强度轨 | 环境和镜头语境影响全局语气与节奏 |
| Playhead | 贯穿所有媒体的共同游标 | 每个信号只在同一时间点被解释 |

`Environment` 不可被画成虚构模型特征。其来源应为可解释视觉量，例如镜头切换、亮度变化、全局运动幅度或人工案例注释，并在 inspector 中注明来源。

## 5. 同步时间线

时间线固定为 5 条轨，均绑定同一 `case_id`、同一 0–T 时基：

1. `VIDEO`：抽帧胶片带；
2. `IPA`：核对过的国际音标 token 和实际 start/end；
3. `VISUAL CUES`：Face / Lip / Environment 标记；
4. `PROSODY`：F0 与能量曲线，分色但共用刻度说明；
5. `SPEECH`：所播放音频的真实峰值波形与 mel 缩略图入口。

播放头由媒体 `currentTime` 驱动。拖动任一轨的时间滑块必须同步更新视频帧、IPA 高亮、F0、能量和波形，不允许各组件独立随机运动。

## 6. 视觉系统

- 基调：深色编辑台 + 中性灰工作区 + 视频/文本/声音/情感的语义色，不使用渐变球或泛蓝紫霓虹背景。
- 动态亮点：沿路径的“数据包”、胶片帧推进、真实波形播放头、IPA token 高亮、图层切换；没有无因果的线条漂浮。
- 排版：主标题在第一屏保持 32–48px；时间码和参数使用 JetBrains Mono；中文使用 Noto Sans SC。
- 布局：桌面在 1440 与 1920 下左到右完整阅读；移动端改为输入轨 -> 方法 -> 输出的纵向顺序，数据流方向仍由编号和箭头明确表达。

## 7. 视觉参考的使用边界

`reference/intro_vtts/image*.png` 的价值是横向任务布局、胶片边界、三输入汇聚和波形输出的表达方式。V2 必须重新绘制自己的界面、动效和图形，不复制参考论文图、角色画面、字体、标注或布局细节。
