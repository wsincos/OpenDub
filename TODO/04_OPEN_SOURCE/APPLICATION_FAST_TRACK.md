# Application Fast Track

## 时间背景

当前日期为 2026-07-26。海报中的第一批申报截止窗口为 2026-07-31，时间不足以在保证许可和真实性的条件下完成全部 Live 模型接入。

因此申报材料采用两层表达：

- **当前已实现基础**：现有 alpha 项目、媒体、API、CLI、Studio、治理和 89 项测试记录。
- **资助拟建设核心**：Task Explorer、三套 Method Canvas、Replay/Comparison 规范和正式展示影片。

申请表不得把本 TODO 中尚未实现的页面写成“已经完成”。

## 五日申报冲刺

### 7 月 26 日：定位和材料冻结

- [ ] 以本规划固定申报名称、摘要和项目边界。
- [ ] 核对申请人、三名以内核心维护者和单位信息。
- [ ] 核对 `https://github.com/wsincos/OpenDub` 为唯一项目仓库。
- [ ] 在申请表中将 Atlas 写为拟建设内容，将 alpha 基础写为现有基础。
- [ ] 确认基础级或重点级，推荐重点级 12,000 元。

### 7 月 27 日：申请表一稿

- [ ] 用 [GRANT_AND_DEMO.md](GRANT_AND_DEMO.md) 重写项目摘要、主要功能和创新性。
- [ ] 技术架构分为 Experience、Content、Runtime、Evidence 四层。
- [ ] 项目基础列出三项论文和固定仓库。
- [ ] 实施计划按 M1-M6 填写。
- [ ] 风险中说明 checkpoint 和素材许可不影响 Concept 主交付。

### 7 月 28 日：可视化设计证据

- [ ] 生成 Task Explorer 高保真静态稿。
- [ ] 生成三套 Method Canvas 的结构线框。
- [ ] 生成 Concept/Replay/Live 状态图。
- [ ] 将设计稿作为规划证据，不伪装成可运行页面。
- [ ] 更新 README 的项目方向和 Roadmap。

### 7 月 29 日：可信 Demo

- [ ] 录制现有 alpha Studio 的真实可用部分。
- [ ] 以静态交互动效原型解释拟建设 Atlas，画面标记 `Design Prototype`。
- [ ] 使用自制或明确许可素材。
- [ ] 影片旁白区分“已经实现”和“资助后完成”。
- [ ] 运行 `make check` 并保存日志摘要。

### 7 月 30 日：交叉审查

- [ ] 负责人审查方法技术表述。
- [ ] 开源负责人审查源代码、权重和素材许可。
- [ ] 非项目成员按三分钟理解测试审查叙事。
- [ ] 检查申请表、README、视频、仓库状态一致。
- [ ] 删除无法由证据支持的“已支持、实时、最佳、完整复现”等表述。

### 7 月 31 日：提交

- [ ] 再次核对申报窗口和在线表单。
- [ ] 上传最终 DOCX/PDF 和视频链接。
- [ ] 检查链接在无登录浏览器中可访问。
- [ ] 保存提交截图、时间和材料 hash。
- [ ] 提交后创建 release 或 tag 固定申报版本。

## 申请表字段映射

| 申请表字段 | 内容来源 |
|---|---|
| 项目名称 | GRANT_AND_DEMO / 最终申报方式 |
| 项目简介 | GRANT_AND_DEMO / 申报摘要 |
| 项目背景 | PROJECT_CHARTER / 要解决的问题 |
| 主要功能 | METHOD_ATLAS_SPEC |
| 技术架构 | SYSTEM_ARCHITECTURE |
| 创新性 | GRANT_AND_DEMO / 为什么不是历史成果打包 |
| 开源基础 | UPSTREAM_BASELINE + 当前 STATUS |
| 计划与里程碑 | IMPLEMENTATION_PLAN |
| 预算 | GRANT_AND_DEMO / 预算建议 |
| 风险 | DECISIONS_AND_RISKS |
| 演示 | DEMO_FILM |

## 当前材料用词

### 可以写“已经完成”

- OpenDub 主仓库和开源治理。
- 项目、素材、授权、时间线、候选、评测、渲染基础。
- FastAPI、CLI 和本地 Web Studio alpha。
- 上游仓库审计和模型准入规则。
- 自动化测试基线。
- Method Atlas 完整产品和技术规划。

### 必须写“计划完成”

- 可运行 Task Explorer。
- 三套可点击 Method Canvas。
- Replay Bundle 和公开 Comparison Lab。
- Live EmoDubber/HPMDubbing/StyleDubber。
- 新正式影片和 `v0.1.0-atlas` 发布。

## 提交前红线

- 不把 GitHub 个人主页当项目仓库。
- 不将三个原仓库并列写进“项目仓库”字段。
- 不声称三模型已经统一运行。
- 不将设计稿称为产品截图。
- 不将历史 Demo 称为 Live。
- 不使用未授权影视片段和名人声音。
- 不因时间紧迫跳过源代码、权重和素材的独立许可说明。
