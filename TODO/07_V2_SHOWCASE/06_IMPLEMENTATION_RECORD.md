# V2 实施记录与当前交付状态

**更新日期：** 2026-07-27
**当前阶段：** 实现、发布级验证、受控来源登记和独立严格审查均已完成。
**发布状态：** `v2.0.0-showcase` 是 V2 正式展示发布；`v0.0.1-alpha.0` 保留为 V1 基线。

本记录用最直接的方式说明：现在仓库里已经有什么、它能说明什么、以及它没有声称什么。它用于项目申请核查，不以计划文字替代已实现事实。

## 1. 现在的产品是什么

OpenDub V2 是一个以任务解释和方法检查为先的开源视频配音平台展示层。首次访问会进入 `/vtts`，先回答视频配音生成的基本结构：

```text
Silent Video + Target Text + Authorized Reference Speech
                         ↓
                 One Complete Method
                         ↓
          Target Speech + Dubbed Video
```

它不是把 HPMDubbing、StyleDubber、EmoDubber 的内部网络层拆开混接成第四个模型。三者仍是独立、完整的方法；平台提供共同的任务解释、样例检查、方法入口、准备工作流和证据边界。

## 2. 已完成的可见体验

| 页面 / 入口 | 已实现内容 | 读者应该得到的结论 |
| --- | --- | --- |
| `/vtts` | 三条输入轨、可播放/暂停/重置的数据流、完整方法、语音和配音视频两类输出 | VTTS 同时受视频、文本和授权参考声音约束 |
| `/vtts` 线索显微镜 | 可切换的 Face、Lip、Environment 观察层 | 口型之外，表情和场景节奏也值得被检查；这些是可解释观察，不是假称内部张量 |
| `/vtts` 同步时间线 | 同一 GT 音频派生的真实波形、F0、能量、log-mel；滑块更新视频位置 | 真实声学特征可以在统一时基下检查 |
| `/examples` | 真人与动画两类 case，各有 GT、HPMDubbing、StyleDubber、EmoDubber 四面板；同一时刻只保留一个播放音轨 | 团队已有多个完整视频配音研究成果，可直接检查其历史样例 |
| `/methods` 与方法 Canvas | 三条完整方法的研究侧重点与结构入口 | 方法选择按创作需求进行，不是把不同论文的组件拼接 |
| Studio / Evidence | 授权输入记录、准备导出、证据与 Compare 门禁 | 当前系统尊重 `Concept / Replay / Live` 的证据差异 |

## 3. 案例资产与真实程度

两个公开 case 定义于 `content/showcases/v2/`：

| case | 视觉类型 | 展示媒体 | 当前状态 |
| --- | --- | --- | --- |
| `human-0` | 真人肖像 | GT、HPMDubbing、StyleDubber、EmoDubber | `Archived research example` |
| `animation-1` | 动画角色 | GT、HPMDubbing、StyleDubber、EmoDubber | `Archived research example` |

每个 case manifest 均含项目负责人确认的 V2 再分发声明、原始本地来源、每条媒体 SHA-256、方法标识、历史结果来源和内容状态。受限原始素材的哈希锚点、受控核验通道和撤回处理记录于 [V2 Controlled Source-Evidence Register](../../docs/rights/showcase-source-evidence-v2.md)。`scripts/build_showcase_features.py` 在核对原始哈希后，才复制批准媒体并从 GT 音频离线导出波形、F0、能量和 log-mel。产物的来源记录位于各 case 的 `provenance.json`。

这两组样例**没有**足以公开核对的 canonical transcript、IPA 对齐或同输入合同。因此它们不进入 Replay、Compare 排名或 Live 声称。页面和影片均固定标示：`Archived research example. Not a fresh OpenDub run.`

`/vtts` 中的英文目标台词与 IPA 是单独、明确标记的 `task notation`，仅解释“目标文本提供说什么和何时说”的任务接口。它们不是对 `human-0` 或 `animation-1` 的转写，不应被当作真实 case 标注。

## 4. V2 视频交付

交付目录：[docs/grant/video/v2/](../../docs/grant/video/v2/)。其中包括：

- `OpenDub_VTTS_Showcase_v2.0.0.mp4`：约 84.2 秒、1920x1080、30 FPS、H.264、AAC；前 20 秒为真实浏览器交互录制；
- 中英双语 SRT 和嵌入字幕轨；
- 中文人工旁白录制稿；
- 事实核查表、交付 manifest、SHA-256 与联系表；
- 可重建脚本 `scripts/build_v2_showcase_film.sh`。

影片的任务流程、线索和时间线镜头来自正在运行的 V2 页面，并由可重建的 Playwright 脚本录制；真人和动画段落使用有界的四格历史样例，且仅播放明确标记的 GT 音轨。影片采用字幕主导和画面内明确标示的非语音说明音轨，以避免把旁白误导为模型生成语音；中文人工录音可在不改变事实边界的条件下按现有文稿加入。

## 5. 关键代码与验证入口

| 位置 | 责任 |
| --- | --- |
| `apps/web/src/features/vtts/VttsTaskStagePage.tsx` | VTTS 任务舞台、流程状态、线索显微镜和时间线 |
| `apps/web/src/features/showcases/ExampleGalleryPage.tsx` | 案例切换、四面板媒体回放和单音轨协调 |
| `apps/web/src/content/showcases.ts` | 由 versioned JSON manifest 驱动的公开案例入口 |
| `src/opendub/showcase/manifest.py` | Python case manifest 验证与 Replay 门禁 |
| `src/opendub/showcase/features.py` | 真实音频特征导出 |
| `scripts/build_showcase_features.py` | 受 manifest 限制的媒体复制、哈希核对与特征构建 |
| `scripts/build_v2_showcase_film.sh` | V2 视频、字幕轨、联系表和哈希的可重建交付 |

最终收口前必须通过：Python 单测与类型检查、前端测试和生产构建、Atlas/registry 验证、case manifest 与来源核对、影片 `ffprobe` 和 SHA-256、五个视口视觉检查，以及独立严格审查达到 `9/10`。

## 6. 当前待完成项

1. [x] 已建立 scoped V2 commit 与候选 tag `v2.0.0-showcase-rc.1`；干净 clone 的 Vite 生产构建、样例媒体与影片 SHA-256 已通过；
2. [x] 严格独立复审第 4 轮为 `9.1 / 10`，达到 `9/10`，报告见 `review/round-04-v2-strict-audit.md`；
3. [x] 已创建正式 V2 tag `v2.0.0-showcase` 并推送公开仓库；随后按远端 tag 重新检出和验证。

这些是发布收口工作，不是新增模型能力。所有新的模型推理、真实 case IPA、Replay 或 Live 均保留在已有证据门之后。
