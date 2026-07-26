# V2 样例、证据与信号资产计划

## 1. 待接入资产

当前参考目录有两组案例：

| case_id | GT | HPMDubbing | StyleDubber | EmoDubber | 视觉类型 |
| --- | --- | --- | --- | --- | --- |
| `human-0` | `reference/example/GT0.mp4` | `0-video1.mp4` | `0-video2.mp4` | `0-video3.mp4` | 真人 |
| `animation-1` | `reference/example/GT1.mp4` | `1-video1.mp4` | `1-video2.mp4` | `1-video3.mp4` | 动画 |

这是本地工作资产清单，不等于已经可以公开发布。当前已按下列 manifest 完成项目负责人确认的 V2 再分发记录，并以 `Archived research example` 而非 Replay 公开；公开范围、适用场景和撤回规则见 [V2 Showcase Media Authorization Record](../../docs/rights/showcase-media-rights-v2.md)。如权利范围变更，必须立即下架媒体。

## 2. 发布前 case manifest

每个案例建立 `content/showcases/v2/<case_id>.json`，最低字段如下：

```json
{
  "case_id": "human-0",
  "display_name": "Human portrait case",
  "content_status": "archived_research_example",
  "rights": {
    "video": "confirmed-by-project-owner",
    "reference_speech": "confirmed-by-project-owner",
    "redistribution": "allowed-for-opendub-v2"
  },
  "input_contract": {
    "target_text_source": "canonical-record",
    "target_text": "verified before publication",
    "ipa_source": "forced-alignment-or-human-reviewed",
    "same_input_across_methods": false
  },
  "artifacts": [
    {"role": "ground_truth", "path": "...", "sha256": "..."},
    {"role": "method_output", "method_id": "hpmdubbing", "path": "...", "sha256": "..."}
  ],
  "provenance": {
    "method_revision": "fixed-before-publication",
    "result_origin": "team-provided historical output"
  }
}
```

`content_status` 的取值：

- `archived_research_example`：结果真实，但尚未满足 OpenDub Replay 合同；
- `replay`：同一输入、权利、方法 revision、输出哈希和说明齐备；
- `blocked`：不在公开网站或申报视频中出现。

案例只有通过 `replay` 检查，才能出现在 Compare 的同输入 A/B/C 模式、播放统计或指标区域。否则只能在 `Example Gallery` 作为有明确边界的研究样例。

## 3. 真实媒体特征管线

从最终允许发布的每一条音频中离线生成特征，所有衍生物存储同源哈希：

```text
source MP4
  -> FFprobe stream contract
  -> FFmpeg PCM WAV
  -> waveform peaks JSON (fixed sample bins)
  -> log-mel PNG / numeric matrix
  -> F0 + energy JSON
  -> duration / loudness / sample-rate manifest
```

输出目录建议：

```text
content/showcases/v2/
  human-0.json
  animation-1.json
apps/web/public/showcases/v2/
  human-0/gt.mp4
  human-0/hpmdubbing.mp4
  human-0/features/gt.waveform.json
  human-0/features/gt.mel.png
  human-0/features/gt.prosody.json
```

实施脚本必须接收 case manifest，而不是直接扫描 `reference/`：

```bash
uv run python scripts/build_showcase_features.py \
  --case content/showcases/v2/human-0.json \
  --output apps/web/public/showcases/v2/human-0
```

脚本必须在 manifest 中写入：输入 SHA-256、FFmpeg 版本、分析窗口、采样率、生成时间和输出 SHA-256。波形、mel 和曲线均由真实音频生成，不能使用 V1 的示意 `MiniWaveform`。

## 4. IPA 与环境标注

1. 找到 LRS3 或团队原始记录中的 canonical transcript；不能根据视频肉眼猜写。
2. 用可重放的对齐器生成初始 IPA 与时间，再由负责人或标注者核对；保留原始文本、音标系统和对齐工具版本。
3. `Environment` 只使用可以复算或人工确认的信号：镜头切点、全局光流强度、场景标签或运动强度。每个标注点均有来源字段。
4. 若案例没有可用文字或环境标注，则它仍可用于示例回放，但不能作为 `/vtts` 的“真实同步时间线”主案例。

### 当前 V2 决定

`human-0` 和 `animation-1` 都明确记录为 `target_text_source: unavailable-for-gallery-only` 与 `ipa_source: unavailable-for-gallery-only`。因此：

- 两组案例在 Gallery 中展示真实 GT / 历史方法媒体、来源哈希和派生声学特征；
- `/vtts` 的英文台词和 IPA token 是独立的 **task notation**，用于解释 VTTS 输入的结构，不是 `human-0` 的转写，也不驱动案例回放；
- V2 不把任何一组案例放入真实 IPA 对齐、同输入比较或 Replay 页面；
- 后续取得 canonical transcript、对齐记录和审校人后，才可创建新的 `timeline_eligible: true` case，而不是修改现有历史案例的事实。

## 5. Example Gallery 的产品规则

### 布局

- 第一屏为 `Human portrait` 与 `Animated character` 两个 case tab；
- 每个 case 的四列固定为 `Ground truth / HPMDubbing / StyleDubber / EmoDubber`；
- 每列是同尺寸视频、方法或 GT 标签、状态、时长、音量和“查看证据”动作；
- 同一时刻只允许一个音轨输出，切换时必须停止其他播放器；
- 鼠标或键盘在某列上悬停时，共享时间游标同步到该列，不能通过不同视频速度制造“看起来更同步”。

### 文案边界

- 有资格的案例：`Verified Replay from an authorized result bundle`；
- 其他案例：`Archived research example. Not a fresh OpenDub run.`；
- 不显示分数、奖杯、最佳标签，除非合格统计和评价合同存在；
- 真实人像和真实声音仅在权利 manifest 允许的公开范围内出现。

## 6. 资产发布策略

先由 `asset-audit` 命令生成媒体清单。只有 manifest 标记 `redistribution: allowed-for-opendub-v2` 的文件进入公开版本控制或发布附件。

- 小型可再分发视频：使用 Git LFS 或 Release Asset，不提交未跟踪大文件到普通 Git 历史；
- 不能再分发的视频：本地 demo 通过受控路径加载，公开版显示脱敏 poster / metadata，申请上传包由负责人按权利范围处理；
- 所有海报帧、波形、mel 继承源视频的发布限制。
