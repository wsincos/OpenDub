# OpenDub Method Atlas Film Production Pack

本目录定义一支可以直接录制的申报影片。影片要让评审先看懂视频配音任务，再看见三套完整方法如何被交互化、可视化和比较，最后相信 OpenDub 是一个有明确证据边界的开源项目。

## 成片定义

- 正式名称：`OpenDub: See How a Scene Becomes a Voice`
- 中文名称：`OpenDub：看见画面如何成为声音`
- 正式版：16:9、1920x1080、30 FPS、2 分 40 秒、中英字幕。
- 预告版：16:9、1920x1080、30 FPS、60 秒。
- 循环版：16:9、1920x1080、30 FPS、30 秒、无旁白。
- 音频交付：48kHz、24bit、立体声，整片目标 `-14 LUFS +/-1 LU`，true peak 不高于 `-1 dBTP`。

## 影片主线

```text
同一画面，不同声音
        |
        v
Video + Text + Reference Speech -> Target Speech
        |
        v
HPMDubbing -> StyleDubber -> EmoDubber
        |
        v
Interactive Method Atlas + Evidence
```

影片不是普通产品宣传片。Task Explorer、Method Canvas、Comparison Lab、Evidence Room 是真实画面主角；动态信息图只用于把观众的注意力从一层带到下一层。

## 文件导航

1. [创意方向](CREATIVE_DIRECTION.md)：画面、声音、动效和禁区。
2. [逐秒母版脚本](MASTER_SCRIPT.md)：旁白、屏幕文字和运行状态分支。
3. [镜头表](SHOTLIST.md)：每一镜需要录制的路由、动作、声音和证据。
4. [录制执行手册](RECORDING_RUNBOOK.md)：冻结环境、素材、录屏和后期交接。
5. [版本剪辑](VERSION_CUTS.md)：2:40、60 秒和 30 秒的精确范围。
6. [事实与交付 QA](TRUTH_AND_QA.md)：模式标签、权利和逐帧核验。
7. [素材权利](ASSET_AND_RIGHTS.md)：视频、声音、音乐、截图和字体登记。
8. [后期规范](POST_PRODUCTION.md)：剪辑、字幕、混音和导出。

## 录制前置条件

- 固定 Git commit、`content-lock.json`、浏览器版本和屏幕尺寸。
- 使用自制、公共领域或明确许可的示例视频、文本和参考声音。
- 每个镜头记录 `Concept`、`Replay`、`Live` 或 `Planned`。
- 没有通过 comparison gate 的结果不得进入同输入 A/B/C 画面。
- Live 镜头只有在当次发布环境实际生成成功时才可使用。

## 影片的专业感来自哪里

- 开场让观众先“听见”画面约束，而不是先读功能列表。
- 每个转场由同一个时间游标、口型、音素或波形推动。
- 三套方法用连续研究演进表达，而不是三个仓库截图。
- 方法节点可点击、时序信号同步移动，体现真实交互性。
- Evidence Room 用源码、论文、许可和 run evidence 收束，不以夸张口号收尾。

## 真实状态规则

| 模式 | 影片可怎么说 | 影片不能怎么说 |
|---|---|---|
| Concept | “论文结构的交互解释” | “模型正在实时输出这个信号” |
| Replay | “来自授权结果包的回放” | “现场生成” |
| Live | “本机真实运行” | 使用历史结果冒充本次运行 |
| Planned | “下一阶段接入方向” | “已支持” |

## 最小团队

- 演示操作：在固定版本执行无错误路径。
- 技术审查：核验论文、状态、权重和证据。
- 导演/剪辑：控制镜头节奏、字幕和声音。

同一人可以兼任演示和剪辑，但技术审查必须由了解三篇论文的人独立完成。
