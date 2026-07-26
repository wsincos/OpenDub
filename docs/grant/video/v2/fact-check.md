# V2 影片事实边界

- `human-0` 与 `animation-1` 的四格均标注为 `Archived research example`；不称为 fresh run、Replay 或同输入公平比较。
- 网页中的波形、F0、能量与 Mel 来自 `apps/web/public/showcases/v2/*/features/*.json`，并可由 `scripts/build_showcase_features.py` 从批准源视频复建。
- `Target speech` 与 `Dubbed video` 在任务舞台中是任务说明，明确标为 `Task illustration · no fresh run`。
- 影片中播放的案例音频来自对应 GT 资产；案例段落画面底部标注 `AUDIBLE: GT`，不由旁白或新生成音频冒充。
- HPMDubbing、StyleDubber 与 EmoDubber 在 OpenDub 的当前运行状态仍为 `Concept` / unavailable；影片不声称 Live 推理可用。
- `assets/clips/` 中的前三段是由 `scripts/capture_v2_web_clips.mjs` 对运行中的浏览器实际录制，而非 PNG 停帧；构建时会裁去 Playwright 的初始空白画面。它们的声音是画面内明确标示的非语音说明音轨，不是模型输出或旁白。
- 当前影片不再展示 Studio 的网络/API 状态，也不以该镜头声明本地准备导出可用。
