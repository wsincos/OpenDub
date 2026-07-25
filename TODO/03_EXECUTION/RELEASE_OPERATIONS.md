# Release and Operations

## 版本体系

### 平台版本

遵循 SemVer：

- Patch：修复且不改变 Schema/Adapter 契约；
- Minor：新增兼容能力、适配器或可选字段；
- Major：破坏 API、Schema 或插件契约。

### Schema 版本

Schema 与平台版本独立。`opendub.project/v1` 在 `v1` 生命周期内只新增可选字段。迁移器从旧版本生成新文件，并保留备份。

### Adapter 版本

Adapter 版本包含：

- 适配器包版本；
- 上游 commit；
- 权重 SHA-256；
- patch set 版本。

只改变权重也必须形成新的可追溯模型版本。

## 模型注册表

每个模型条目必须包含以下字段：

| 字段 | 类型 | 发布要求 |
|---|---|---|
| `id` | string | 使用 `publisher/model-name`，发布后不复用 |
| `display_name` | string | 与模型卡一致 |
| `maturity` | enum | `planned`、`experimental` 或 `stable` |
| `adapter_package` | string | 可安装的 Python 包名 |
| `source.repository` | URL | 精确上游仓库 |
| `source.commit` | 40 位十六进制字符串 | Experimental/Stable 必填 |
| `artifacts[].role` | enum | `acoustic_model`、`vocoder`、`encoder` 等 |
| `artifacts[].sha256` | 64 位十六进制字符串 | 可下载制品必填 |
| `runtime.isolation` | enum | `in_process`、`subprocess` 或 `container` |
| `capabilities_file` | path | 必须指向随适配器发布的 `adapter.yaml` |

验证脚本会拒绝空 commit、空哈希、浮动分支或格式不正确的可发布条目。审计尚未完成的模型保持 `planned`，且不提供可下载 artifacts。

## 制品

`v0.1.0` 发布：

- Python 包 `opendub`；
- Web 静态制品；
- API、Web、Worker 容器镜像；
- Docker Compose；
- JSON Schema；
- SBOM；
- 第三方许可证报告；
- 示例项目；
- 校验和清单；
- 源码归档；
- 发布说明。

模型权重不默认打包，使用 Registry 下载并验证。许可允许且体积合理时，可作为单独 Release Asset 发布。

## CI 分层

### Pull Request

- 格式与静态检查；
- 单元、契约、集成测试；
- Web 单元与 TestAdapter E2E；
- Schema 差异；
- 文档链接；
- 许可和 Registry 校验；
- secret 与依赖扫描。

### Main

- PR 全部检查；
- 构建容器；
- 运行容器 smoke；
- 生成开发制品。

### Release Candidate

- 受控 GPU 真实模型 smoke；
- 全量 Playwright；
- 授权示例；
- 安装文档验证；
- SBOM 和镜像扫描；
- 人工视觉 QA。

## 日志与诊断

- 结构化 JSON 日志写入状态目录；
- 控制台日志使用人类可读格式；
- 每个 API 请求和任务有 `trace_id`；
- 模型 stderr 单独保存并限制大小；
- 日志轮转，默认保留 7 天或 1GB 中先达到者；
- `doctor --report` 输出环境、版本、错误码和脱敏日志。

## 数据保留

- 项目数据由用户明确删除；
- `.partial` 超过 24 小时可由清理命令删除；
- 未引用候选默认保留，由项目设置控制；
- 共享权重只有显式 `opendub models prune` 才删除；
- 导出不会自动删除生成来源。

## 模型装载与显存

- 单 GPU 默认一个模型生成任务；
- 同模型连续任务复用已装载权重；
- 空闲 5 分钟后默认释放；
- 切换模型前主动释放并同步 CUDA；
- OOM 时记录请求、模型与显存摘要，释放后允许用户降低候选数或切换设置重试；
- 不自动降低精度或质量而不通知用户。

## 故障恢复

- 项目清单采用原子保存；
- 任务阶段结果采用 `.partial → final`；
- 重启后运行中任务变为 interrupted；
- 用户可以从最后成功阶段重试；
- SQLite 损坏时从项目目录重建；
- 模型缓存损坏时根据哈希删除单一制品并重新下载；
- 原始输入永不被转码覆盖。

## 发布步骤

1. 冻结 milestone，关闭或移动未完成 Issue。
2. 更新 CHANGELOG、模型状态、支持矩阵和已知限制。
3. 执行完整验证并提交报告。
4. 从干净环境构建制品和 SBOM。
5. 使用候选标签运行安装测试。
6. 创建签名正式标签。
7. 发布 GitHub Release、容器和 Python 包。
8. 校验公开制品哈希与 Registry。
9. 在新的干净环境执行一次公开安装。
10. 发布公告和升级说明。

## 回滚

- 不删除有问题的 Release；标记为 withdrawn，并说明原因。
- 容器标签保留不可变 digest。
- Registry 可以下架自动下载，但保留历史记录和已安装用户的诊断信息。
- 紧急修复从受影响标签分支，发布 patch 版本。

## 运行支持

支持入口：

- GitHub Discussions：安装、使用和模型讨论；
- GitHub Issues：可复现缺陷和功能请求；
- Security 私下渠道：安全和隐私；
- 模型上游问题优先判断属于 Adapter 还是上游，再引导提交。

Issue 模板要求版本、运行模式、`doctor --report` 和最小复现；禁止要求用户上传未脱敏视频或声音。
