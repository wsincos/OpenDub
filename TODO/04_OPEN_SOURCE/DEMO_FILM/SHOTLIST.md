# Shot List

## Capture Baseline

- Screen capture: 3840x2160 at 60 FPS; editorial master: 1920x1080 at 30 FPS.
- Browser zoom: 100%; OpenDub controls scale itself.
- Recording viewport: 1920x1080 for full canvas, 1440x900 for supporting screenshots.
- Every shot log records route, Git commit, content-lock hash, case ID and content mode.

| # | Time | Route / Action | Required evidence | Sound | Transition |
|---:|---|---|---|---|---|
| 01 | 00:00-00:03 | Same video, flat reference reading | rights ID and source label | source A only | hard return |
| 02 | 00:03-00:06 | Same video, target speech | Replay or Live badge | source B only | playhead flash |
| 03 | 00:06-00:09 | Title and timeline | title render | no music | fine-line wipe |
| 04 | 00:09-00:14 | `/explore`, select Video | case manifest | voiceover | direct cut |
| 05 | 00:14-00:19 | select Text and phonemes | transcript timing | voiceover | cursor match |
| 06 | 00:19-00:24 | select Reference Speech | voice rights | voiceover | cursor match |
| 07 | 00:24-00:34 | Generated Speech to Dubbed Video | output separation | voiceover | tab transition |
| 08 | 00:34-00:41 | `/methods/hpmdubbing`, Lip | paper anchor | voiceover | graph focus |
| 09 | 00:41-00:48 | HPM Face and Scene | F0/Energy and Scene signal mode | voiceover | pinned tracks |
| 10 | 00:48-00:56 | HPM full path | method manifest | voiceover | line follow |
| 11 | 00:56-01:04 | `/methods/styledubber`, frame view | paper anchor | voiceover | scale fold |
| 12 | 01:04-01:11 | Style phoneme view and PLA | token timing | voiceover | cursor match |
| 13 | 01:11-01:17 | Style MPA and USL | mode label | voiceover | graph focus |
| 14 | 01:17-01:24 | `/methods/emodubber`, LPA and PE | paper anchor | voiceover | line follow |
| 15 | 01:24-01:31 | Speaker identity and FUEC | source/mode label | voiceover | graph focus |
| 16 | 01:31-01:38 | emotion control | only actual available controls | voiceover | slider cue |
| 17A | 01:38-01:50 | `/compare/:caseId`, candidate A/B/C | comparison gate pass | candidates only | hard cuts |
| 18A | 01:50-02:01 | blind reveal and metrics | equal input hashes | voiceover | compact fade |
| 17B | 01:38-02:01 | comparison gate explanation | failed gate reason | voiceover | no ranking |
| 19 | 02:01-02:12 | `/evidence`, HPM/Style/Emo rows | paper, commit, license | voiceover | vertical scan |
| 20 | 02:12-02:21 | mode matrix and run/replay details | content status | voiceover | time cursor |
| 21 | 02:21-02:36 | return to dubbed video | final media rights | voiceover then output | gentle fade |
| 22 | 02:36-02:40 | End card | repository URL | tail tone | hold |

Use branch A only if the public case passes the comparison gate. Branch B is a first-class professional scene, not a failure screen.

## Recording Names

```text
YYYYMMDD_opendub_s01_flat-source_4k60.mov
YYYYMMDD_opendub_s02_target-speech_4k60.mov
YYYYMMDD_opendub_explore_take01_4k60.mov
YYYYMMDD_opendub_hpm-canvas_take01_4k60.mov
YYYYMMDD_opendub_style-canvas_take01_4k60.mov
YYYYMMDD_opendub_emo-canvas_take01_4k60.mov
YYYYMMDD_opendub_compare_take01_4k60.mov
YYYYMMDD_opendub_evidence_take01_4k60.mov
YYYYMMDD_opendub_vo_master_48k24.wav
```

## Capture Notes

- 每个交互镜头前后留 2 秒稳定帧。
- Method Canvas 录制时只高亮一条主路径，避免观众同时追踪所有边。
- 概念曲线在录屏中保持 `Illustrative`，不在后期擦除标签。
- 片尾仓库地址使用 `github.com/wsincos/OpenDub`。
