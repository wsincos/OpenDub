# Method Atlas Quality Plan

## 质量目标

质量不是页面无报错，而是同时满足：

1. 任务和方法表述准确。
2. Concept、Replay、Live 状态可信。
3. 时间同步、播放和比较行为正确。
4. 五个目标视口可读、可操作、无重叠。
5. 素材、声音、论文、代码和权重来源可追溯。
6. 没有 GPU 和 API 时核心 Atlas 仍然完整。

## 自动化层级

### Python 单元测试

覆盖：

- Atlas Pydantic models。
- graph referential integrity。
- asset path、hash、rights。
- Concept illustrative rules。
- Replay pack 和 comparison gate。
- author review 和 content lock。

目标：`src/opendub/atlas` 分支覆盖率不低于 90%。

### Web 单元测试

覆盖：

- content loader 和 runtime guards。
- TimelineController。
- method layout。
- signal renderer registry。
- comparison media registry。
- metric compatibility policy。
- blind order 和 report export。

必须使用确定性 fixture，不使用网络和真实浏览器媒体时钟。

### Web 组件测试

覆盖：

- Task Explorer 三项输入和两类输出。
- Method Inspector 的完整字段。
- 缺失信号降级。
- status honesty。
- Compare 的 N/A、Unavailable 和 blind reveal。

### Python 集成测试

覆盖：

- 真实 FFprobe/FFmpeg 媒体探测。
- Replay Bundle pack/inspect。
- Live run 到 Replay 导出。
- API 不可用和权重缺失。

### Playwright E2E

覆盖：

- `/explore` 完整导览和手动接管。
- `/methods` 到三个深链接。
- 节点选择、信号固定和 Evidence。
- Comparison 互斥播放和盲听。
- Studio 基线不回归。
- 浏览器刷新、后退、离线静态构建。

## 内容正确性

### 论文一致性检查

每个方法建立节点级核验表：

- 节点名称。
- 问题描述。
- consumes/produces。
- 入边/出边。
- 可视化信号。
- 论文章节。
- 代码入口。
- reviewer decision。

发布构建要求三套方法所有核心节点均为 `approved` 或修改后 `approved`。

### 禁用表达扫描

CI 扫描公开内容中的高风险词：

- `best model`
- `perfect lip sync`
- `real-time`
- `live generation`
- `state of the art`

出现后必须在 allowlist 中附证据和限定范围，否则构建失败。

### 状态检查

- `Live` 必须有 ready runtime、固定 commit、weight hash 和 real smoke。
- `Replay` 必须有合法 bundle、hash 和 rights。
- `Concept` 数值示意必须有 `Illustrative`。
- `Planned` 不提供可点击运行按钮。

## 时间与媒体正确性

### 时间基准

- manifest 时间为整数微秒。
- 视频使用真实 PTS。
- 音频使用 sample 和 sample rate。
- token interval 必须满足 `0 <= start_us < end_us <= case.duration_us`。
- 等间隔信号的最后一个 sample 不得越过案例范围超过一个 hop。

### 同步门槛

- seek 后活动音频与全局游标误差小于 50ms。
- 候选切换后误差小于 50ms。
- 视频帧、token 高亮和信号游标在一个浏览器动画帧内更新。
- 页面隐藏或路由变化后所有媒体暂停。
- 任意时刻最多一个比较音频处于播放状态。

### 媒体有效性

- 视频可解码且至少包含 10 个非黑帧。
- 音频包含有限 sample，非全静音，采样率与 manifest 一致。
- 波形 peaks 与源音频时长一致。
- 代理文件不覆盖原始 hash。

## 视觉 QA

### 视口

- 1920x1080
- 1440x900
- 1280x720
- 768x1024
- 390x844

### 必查项目

- 无横向页面溢出。
- 节点和边不遮挡核心文字。
- 最长方法和组件名完整换行。
- 图谱 Canvas 有非背景像素。
- 时间轴、播放头和媒体有稳定尺寸。
- 没有空白视频、频谱或波形。
- status 标签始终可见。
- hover、focus 和 selected 不改变布局尺寸。
- 弹层不超出视口。

截图基线只用于发现回归，人工检查必须确认媒体内容和语义没有错位。

## 可访问性

- WCAG AA 对比度。
- 所有图谱节点可聚焦并可用 Enter/Space 选择。
- Space、方向键、Home、End 的行为有测试。
- focus 不被 Canvas 或 Drawer 吞掉。
- status 不只靠颜色。
- 波形、曲线和 heatmap 有文本摘要。
- `prefers-reduced-motion` 无路径飞行动画。
- 自动导览有暂停、前后和重播。

使用 axe 扫描 `/explore`、三个方法页、Compare 和 Evidence，阻断 critical 和 serious 问题。

## 性能

在生产构建、关闭 DevTools 条件下测试：

- 首次内容绘制目标 < 1.5s。
- 首屏关键 JS gzip 目标 < 250KB。
- 方法图交互响应 < 100ms。
- 1440x900 游标拖动 > 50 FPS。
- 单个初始 manifest < 200KB。
- 长信号不创建超过 2,000 个 DOM 节点。
- 重复切换候选不重复下载缓存媒体。

如果超标：

1. 检查路由拆包。
2. 检查 JSON 是否加载了完整数值信号。
3. 将大数组改为二进制和按需加载。
4. 将长波形、频谱和矩阵移到 Canvas/WebGL。

## 安全与许可

- 内容 path traversal 测试。
- manifest 富文本消毒测试。
- 公开构建不得包含本地绝对路径。
- Replay 只有 `publicDisplayAllowed=true` 才可展示。
- 下载包另需 `redistributionAllowed=true`。
- 参考声音授权与每个结果关联。
- 外部 URL 使用 allowlisted `https`。

## 申报影片 QA

- 每个镜头记录路由、模式、案例、commit 和 content-lock。
- 每句旁白有 evidence。
- Replay/Concept/Live 标签在画面中可读。
- 不通过剪辑制造不存在的实时速度。
- 不同输入结果不进入 A/B/C 同输入叙事。
- 音频响度一致但不改变原始结果文件。
- 中文字幕在 1080p 和手机预览中可读。

## 发布检查命令

```bash
make check
uv run opendub atlas validate content
uv run pytest --cov=opendub.atlas --cov-report=term-missing
pnpm --filter @opendub/web test -- --run
pnpm --filter @opendub/web build
pnpm --filter @opendub/web exec playwright test
uv run python scripts/check_docs_links.py
git diff --check
```

任何阻断失败都不得通过“只在本机看起来正常”豁免。
