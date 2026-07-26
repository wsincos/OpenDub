# V2 网页实施计划

## 1. 代码边界与文件职责

| 文件或目录 | 职责 |
| --- | --- |
| `apps/web/src/features/vtts/VttsTaskStagePage.tsx` | `/vtts` 的页面编排、案例选择、播放状态、进入 Atlas 的动作 |
| `apps/web/src/features/vtts/VttsTaskFlow.tsx` | 三输入、完整方法、双输出的 SVG 数据流和动画状态机 |
| `apps/web/src/features/vtts/SynchronizedCueMicroscope.tsx` | Face、Lip、Environment 的可切换检查器 |
| `apps/web/src/features/vtts/SynchronizedTimeline.tsx` | 同源视频、IPA、视觉线索、韵律和波形时间线 |
| `apps/web/src/features/showcases/ExampleGalleryPage.tsx` | 真人 / 动画案例和四列媒体回放 |
| `apps/web/src/content/showcases.ts` | 解析、校验和暴露已准入的 showcase manifest |
| `content/showcases/v2/*.json` | 可审计案例元数据，不放在 React JSX 中 |
| `scripts/build_showcase_features.py` | 为批准案例计算特征和写入哈希 |
| `apps/web/src/features/vtts/*.test.tsx` | 行为、可访问性、状态和事实边界组件测试 |
| `apps/web/src/features/vtts/vtts-task-stage.css` | V2 的媒体舞台、流程线、时间线和响应式样式 |

现有 `TaskExplorerPage` 不立即删除。实现时先将其替换为从 `/vtts` 可进入的详细视图，待 V2 完整 QA 通过后再确定是否将 `/explore` 重定向或保留为 `Explorer detail`。

## 2. 实施任务

### W1：建立带验证的 Showcase 内容模型（已完成）

- [x] 新增 `ShowcaseArtifact`、`ShowcaseCase`、`ShowcaseStatus` TypeScript 类型，并直接加载 versioned case JSON；
- [x] 新增 Python manifest validator，拒绝没有再分发许可的公共案例，拒绝不满足同输入合同的 Replay；
- [x] 写失败测试：无再分发许可的案例不能进入公共 Gallery；
- [x] 写失败测试：`archived_research_example` 不能被声明为 Replay；
- [x] 加载两组经项目负责人确认的案例，并在界面固定显示历史样例状态。当前没有无资产空状态，因为 V2 的公开资产已由 manifest 门禁。

### W2：实现 VTTS 流程动画（已完成）

- [x] 写组件测试：默认显示三输入、一完整方法、目标语音和配音视频；
- [x] 用原生 SVG 路径、状态机和沿线数据包实现可播放、暂停、重置的任务解释；不引入粒子或 3D 库；
- [x] 任务流程与输出固定标示 `Task illustration · no fresh run`；真实 GT 特征另有来源标示；
- [x] CSS reduced-motion 回退取消流程路径动画，保留可检查终态；
- [ ] **后续增强，不进入本次申报承诺：** 为每一个流程阶段补充计时器序列和 reduced-motion 的端到端自动化测试。

### W3：实现线索显微镜与同步时间线（核心完成，案例 IPA 有意受限）

- [x] 写测试：Face、Lip、Environment 三个图层可以独立切换，状态写入 ARIA；
- [x] 共享时间滑块更新同一案例视频的 `currentTime` 和可见播放头；
- [x] 显示同源 GT 的 F0、能量、波形和 log-mel，并直接注明 `human-0 / GT audio`；
- [x] 使用固定轨道尺寸和 SVG 裁剪，禁止曲线改变布局；
- [x] 视觉与声学素材均由准入 case 和 `build_showcase_features.py` 生成；
- [x] 英文 IPA 在页面上标为 `task notation`，不伪称为 `human-0` 或 `animation-1` 的真实标注；真实 case IPA 等待 canonical transcript 后补充。

### W4：实现真实 Example Gallery（已完成）

- [x] 写测试：Human 和 Animated case tab 均可切换；
- [x] 写测试：四个视频面板有 GT / 方法标签、内容状态和证据链接；
- [x] 写测试：播放一个面板会暂停另外三个面板；
- [x] 用 `<video>`、明确用户播放动作和单音轨协调器实现媒体控制；
- [x] 用 `Archived research example` / `Verified Replay` 两种状态文本控制事实边界；当前两组案例均为前者且没有 Compare 排名入口；
- [x] 页面仅从通过再分发条件的 JSON manifest 加载媒体；Python 检查不允许没有来源、哈希或权利声明的案例通过。

### W5：衔接现有 Atlas 与导航（已完成）

- [x] 在全局导航加入 `Task` 和 `Examples`，默认路由指向 `/vtts`；
- [x] 中央完整方法与 Example Gallery 的方法标签进入 `/methods` 和对应 Canvas；
- [x] 保持现有 `Prepare project`、Studio、Evidence、Compare 的 Concept / Replay / Live 规则不变；
- [x] 更新 README、项目当前状态、产品说明和 V2 文档，清楚区分 V1 tag 与 V2 Showcase 工作树；
- [x] V1 视频与申报 Word 不修改版本号；V2 视频独立位于 `docs/grant/video/v2/`。

## 3. 视觉实现标准

- 禁止多层卡片嵌套；流程舞台、示例画廊和时间线都是全宽工作区；
- 视频和输出区域使用固定 `aspect-ratio`；移动端不允许文字遮住播放器或时间轴；
- 使用 lucide 图标作为播放、暂停、重置、缩放和证据动作；文字按钮只表示明确命令；
- 颜色用于模态含义：Video 蓝、Text 紫、Reference Voice 绿、Prosody 橙、Emotion 红、Output 深绿；
- 动画总是能被停止，不依赖鼠标悬停才能理解，也不以循环跳动冒充音频特征。

## 4. 完成后的代码验证

```bash
.venv/bin/pytest -q
.venv/bin/mypy src/opendub
.venv/bin/ruff check src tests
.venv/bin/opendub atlas validate --content content
.venv/bin/python scripts/verify_registry.py model-registry/upstreams.yaml
npm --prefix apps/web run test -- --run
npm --prefix apps/web run build
.venv/bin/python scripts/build_showcase_features.py --verify-only \
  --case content/showcases/v2/human-0.json --output apps/web/public/showcases/v2/human-0
.venv/bin/python scripts/build_showcase_features.py --verify-only \
  --case content/showcases/v2/animation-1.json --output apps/web/public/showcases/v2/animation-1
```

视觉审查必须覆盖 `1920x1080`、`1440x900`、`1280x720`、`768x1024` 与 `390x844`，并在真实案例播放、暂停、切换、reduced-motion 和无资产空状态下检查。
