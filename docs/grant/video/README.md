# OpenDub 申报演示视频交付

本目录保存 `v0.0.1-alpha.0` 的可复核申报演示视频及其字幕、校验和与交付清单。

## 文件与用途

| 文件 | 用途 |
| --- | --- |
| `OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4` | 110 秒、1920x1080、30 FPS 的最终申报成片 |
| `OpenDub_Application_Walkthrough_v0.0.1-alpha.0_CN_EN.srt` | 片中使用的简体中文 / 英文双语字幕 |
| `narration.zh-CN.txt` | 中文旁白的逐句文本，用于事实复核和重录 |
| `delivery-manifest.json` | 录制版本、事实边界、来源和校验信息 |
| `OpenDub_Application_Walkthrough_v0.0.1-alpha.0.sha256` | 视频 SHA-256 校验和 |

## 内容状态与事实边界

- 画面由本仓库当前 Web 界面在本地 Chromium 中录制；每个页面对应 `/explore`、`/methods`、`/methods/emodubber`、`/studio`、`/evidence` 或 `/compare`。
- 中文旁白是用于说明产品流程的合成旁白，不是 OpenDub、HPMDubbing、StyleDubber 或 EmoDubber 生成的样例音频。
- 视频没有使用真实人物声音、未授权影视素材、私有 checkpoint、模型运行结果、虚构指标或虚构比较结论。
- `CONCEPT` 仅表示机制解释和界面概念；`Replay` 与 `Live` 只有满足 [证据索引](../evidence-index.md) 的准入条件后才可以在平台中出现。

## 审核与申请使用

申请表的“项目演示视频”字段应填写：

```text
随申报材料附送：docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4
版本与校验信息：docs/grant/video/delivery-manifest.json
仓库发布版本：v0.0.1-alpha.0
```

录制脚本和逐句边界见 [演示脚本](../demo-script.md)。视频发布后，必须核对视频版本、Git tag、Word 表和 `delivery-manifest.json` 使用相同版本标识。
