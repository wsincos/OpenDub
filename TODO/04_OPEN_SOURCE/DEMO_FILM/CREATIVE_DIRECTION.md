# Creative Direction

## 创作命题

> 让观众亲眼看见：一段视频不是背景，而是决定声音节奏、风格和情感的条件。

开场句：`同一句台词，画面决定它该怎样被说出。`
结束句：`OpenDub. See how a scene becomes a voice.`

## 画面语言

影片在三种画面之间切换：

- 授权视频片段：给观众真实情感和口型对象。
- OpenDub 交互界面：展示可操作的 Task Explorer、Method Canvas、Comparison 和 Evidence。
- 精密信息图：只放大正在被点击的输入、节点或时序信号。

主视觉是贯穿全片的时间游标。它从视频帧穿过 Lip ROI、Face、phoneme、F0、mel 和 waveform，最终到达目标语音。画面不使用 AI 大脑、粒子、数字雨、发光球或无含义的网络动画。

## 色彩和动效

- Video `#1877C9`，Text `#7656C1`，Voice `#12836F`，Prosody `#D47A22`，Emotion `#C84B61`，Output `#2D8A4E`。
- 信息图背景保持 `#F3F5F6`，正文使用 `#111315`。
- 节点高亮 180ms，数据路径推进 240 至 360ms，图形不会弹跳或旋转。
- `Concept` 用细虚线和 `Illustrative` 标签，`Replay` 用实线和 asset badge，`Live` 用 run badge。
- 每一章最多一个转场。优先用嘴部动作、波形峰值和时间游标 match cut。

## 声音设计

- 开场：不放音乐，先后听两段具有相同响度基准的声音。
- 任务解释：极低音量的脉冲，跟随时间游标而非制造悬疑。
- Method Canvas：轻微 click 和短 whoosh，音量低于旁白 18dB 以上。
- Comparison：音乐完全退出，让观众自己判断。
- 结尾：保留一声干净的尾音和约四秒片尾静帧。

## 示例素材

使用团队自制、10 秒以内的人物近景。优先选择一个角色从平静到惊喜或坚定的明确表情变化，画面中嘴部清晰、背景无商标。台词使用原创短句：

> `你终于来了。`

参考声音由同一演员在安静环境录制。需要肖像、声音、生成展示、申报和 GitHub 公开展示的授权。

## 关键时刻

1. 冷开场：相同画面回放两次，声音改变观众对表情的理解。
2. 任务展开：Video、Text、Reference Speech 依次接入同一时间线。
3. HPM：Lip、Face、Scene 三层视觉线索同时亮起。
4. Style：画面从 frame view 折叠为 phoneme view，再拉出 utterance style 带。
5. Emo：用户滑动情感强度，界面明确显示 Concept 或 Replay 状态。
6. Compare：同输入结果才允许 A/B/C 互斥播放；否则展示“comparison gate”而不是伪对比。
7. Evidence：三篇论文、固定 commit、许可和模式状态合流。

## 禁止项

- 不使用商业影视片段、名人声音和来源不明音乐。
- 不用后期补出的波形和曲线暗示模型中间输出。
- 不用不同输入的 Demo 做横向优劣对比。
- 不在没有真实模型运行时录制“GPU 正在生成”的画面。
- 不在同一镜头塞入超过一条可读信息。
