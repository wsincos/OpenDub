# V2 反馈到需求的可追溯表

## 1. 输入反馈的设计解释

| 用户反馈 | V2 的确定要求 | 验收方式 |
| --- | --- | --- |
| 首屏没有讲清 VTTS | 新增 `/vtts` 任务入口，先于 `/explore` 进入 | 新用户测试能复述三输入、一完整方法、目标语音和配音视频 |
| 流程图死板 | 使用可播放 SVG/Canvas 数据流：视频胶片、台词、参考音频沿独立路径进入方法，再向目标语音和配音视频推进 | 暂停后可检查每条路径，动画遵从 reduced-motion |
| 需要电影胶片、真实波形和横向流向 | 视频轨使用原始可授权帧的横向胶片带，音频轨使用同源波形，整体采用左到右流向 | 不复用参考图像本身；页面截图清楚呈现原创组件 |
| `One scene...` 要加入 Environment | 视觉提示改为 `Face / Lip / Environment`，每项有解释与时间关联 | 三个开关、标签和 inspector 都可键盘操作 |
| 时间线的音素与声学图不真实 | F0 / 能量、波形、mel 必须从同一案例音频构建；IPA 只有在有已核对台词时才可作为 case 标注 | 所有真实信号标有 `case_id` 和生成脚本版本；任务示意 IPA 必须直说是示意 |
| 需要真人与动画真实样例 | 新建 Example Gallery：两组案例各展示 GT、HPMDubbing、StyleDubber、EmoDubber | 播放清单、哈希、来源、权利、方法 revision 均可打开查看 |
| 网页太简陋、太 AI | 从卡片堆叠改为“电影化研究仪器”：全宽媒体舞台、精确时间轴、可见信号、低装饰高信息密度 | 1920、1440、1280、768、390 视口截图通过人工设计审查 |
| 视频缺少震撼和结果 | V2 视频以真实浏览器录制的动态 VTTS 任务开场、以两组真实样例为结果锚点、以证据门为可信收束 | 84 秒影片通过事实核查、音画 QA 和独立审计 |

## 2. V2 的用户叙事

V2 只回答一个问题：

> **一段无声画面，如何在目标台词与授权声音条件下，成为时间、口型、情绪和场景都合理的配音？**

叙事必须按如下逻辑出现：

```text
Silent video observes Face, Lip, Environment
Target text supplies words and phoneme timing
Authorized reference speech supplies permitted voice identity
One complete research method resolves the constraints
Target speech is muxed with the original video into a dubbed video
```

三种方法随后只回答“面对不同创作重点，应先看哪条完整路径”：

- HPMDubbing：视觉韵律与场景节奏；
- StyleDubber：发音清晰度与角色风格；
- EmoDubber：显式情感方向。

## 3. 版本与范围锁

### 进入 V2 的内容

- 动态 VTTS 任务入口和升级后的 Explore 体验；
- 真实、授权、可审计的两组案例展台；
- 真实媒体导出的波形、mel、F0 / 能量；IPA 时间标注仅在取得 canonical transcript 后进入 case 时间线；
- V2 浏览器录屏、非语音说明音轨、样例声音混音、字幕、校验和和申报材料更新；
- 现有 Atlas、Canvas、Studio、Evidence 的视觉衔接与录屏路径优化。

### 不进入 V2 的内容

- 不训练新模型；
- 不拆分或混接 HPMDubbing、StyleDubber、EmoDubber 内部模块；
- 不在证据不足时把历史样例提升为 Replay 或 Live；
- 不加入无来源的“神经网络粒子”、随机跳动的波形、虚构性能数字或未授权影视素材；
- 不用通用渐变 Hero、玻璃卡片、大号营销口号替代任务解释。

## 4. 关键风险与先决条件

| 风险 | 处理规则 | 阻塞对象 |
| --- | --- | --- |
| 例示视频的再分发或公开展示权利不清 | 先写入 asset manifest；无书面或可追溯授权时仅在本地审查，不进入公开仓库和申报视频 | 样例发布、视频成片 |
| GT 与三种方法不是同一输入条件 | 作为 `Archived research example` 展示，不称公平比较；只有输入合同齐备时可升为 `Replay` | Compare 页面与指标 |
| 没有已核对的文字 / IPA | 从案例原始数据或负责人确认文本取得；禁止依据画面猜写台词。未取得前只使用显式标记的任务示意 | case 级时间线与 Replay 声称 |
| 音频特征与视频不一致 | 所有波形、mel、F0 都由具体音频 SHA-256 离线生成 | Task Explorer 信号、影片镜头 |
| 动画影响可读性或录像稳定 | 采用有限状态机、可暂停和 deterministic 导览；录制使用固定浏览器与固定 `tour=film` 状态 | 页面发布、V2 视频 |
