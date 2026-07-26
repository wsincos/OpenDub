# V2 质量、发布与复审计划

## 1. 分层验收

### 内容与权利

- [x] 每条当前公开视频、音频、海报帧、波形、mel 均能追溯到 manifest；任务示意 IPA 不计入 case 资产；
- [x] 每个 manifest 包含文件 SHA-256、展示许可、方法来源和内容状态；
- [x] 无完整输入合同时，页面和视频使用 `Archived research example` 而不是 Replay；
- [x] 当前媒体使用项目负责人声明的 V2 再分发许可；独立审查仍须确认该声明覆盖申请提交与公开仓库；
- [x] `reference/` 只作为本地输入，不进入版本控制；公开包仅含通过 manifest 的副本和派生资产。

### 功能与可访问性

- [x] VTTS 流程状态机、暂停、重置、键盘可达性有组件测试；reduced-motion 提供静态检查终态并在人工 QA 中核查；
- [x] 同步时间线的 GT 特征、视频位置和声学来源一致；IPA 明确是独立任务示意，不伪称 case 标注；
- [x] Gallery 只允许一个媒体音轨播放；
- [x] Case 状态准确限制 Compare / Replay 入口；
- [x] 现有 Atlas、Studio、Evidence 与 API 测试不回归。

### 视觉与录制

- [x] 对 1920、1440、1280、768、390 五个视口生成截图；
- [x] 检查流程箭头、胶片孔、视频裁切、任务 IPA、时间码、字幕和移动端布局；
- [x] 流程动画可暂停；录制脚本以确定性 Playwright 操作重建任务流、线索切换与时间线拖动；
- [x] 视频抽帧覆盖镜头表所有段落，检查不出现空白帧、错误 Studio 状态、裁切和重叠；
- [x] 中英双语字幕、字幕主导文稿和嵌入字幕流文本相符。

### 构建与发布

- [x] `make check`、Registry、Manifest、showcase feature verify、Web build 全部通过；
- [x] V2 文件使用新的版本名与 SHA-256；V1 视频、V1 manifest、原 tag 和审核报告不被覆盖；
- [x] 生成 `CHANGELOG` 条目、README 入口、V2 状态说明和申请材料差异清单；
- [x] 使用候选 tag `v2.0.0-showcase-rc.1` 创建干净 clone；Vite 生产构建、样例媒体与 V2 视频 SHA-256 均通过；正式 tag `v2.0.0-showcase` 冻结发布内容；
- [x] 独立审查者已对任务准确性、样例边界、视觉完成度和申报叙事重新评分：第 4 轮严格审核为 `9.1 / 10`，达到发布门槛，记录见 `review/round-04-v2-strict-audit.md`。

## 2. 发布门禁

V2 只有在以下命令与人工记录共同通过时才发布：

```bash
.venv/bin/pytest -q
.venv/bin/mypy src/opendub
.venv/bin/ruff check src tests
.venv/bin/opendub atlas validate --content content
.venv/bin/python scripts/verify_registry.py model-registry/upstreams.yaml
.venv/bin/python scripts/build_showcase_features.py --verify-only \
  --case content/showcases/v2/human-0.json --output apps/web/public/showcases/v2/human-0
.venv/bin/python scripts/build_showcase_features.py --verify-only \
  --case content/showcases/v2/animation-1.json --output apps/web/public/showcases/v2/animation-1
npm --prefix apps/web run build
ffprobe -v error -show_entries format=duration:stream=codec_name,codec_type,width,height,r_frame_rate \
  docs/grant/video/v2/OpenDub_VTTS_Showcase_v2.0.0.mp4
```

视频核验还必须检查：视频 SHA-256、字幕 SHA-256、字幕时码覆盖、音频响度、所有样例 asset ID、`delivery-manifest.json` 的 commit/tag 一致性。

## 3. 最终独立审查问题

审查者在不阅读代码前必须能回答：

1. VTTS 的输入、完整方法和输出分别是什么？
2. Face、Lip、Environment 为什么需要同一时间轴？
3. 真实示例来自哪里，GT 和各方法输出分别是什么状态？
4. 三种完整方法如何按需求选择，为什么不是拼接模型？
5. 为什么当前某些方法仍不是 Live，平台如何诚实处理这一点？

若任一问题无法从 V2 页面或视频中清楚回答，V2 不可发布。
