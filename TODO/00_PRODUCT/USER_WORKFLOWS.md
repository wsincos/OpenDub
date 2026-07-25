# User Workflows

## Workflow A：评审理解视频配音任务

1. 打开 `/explore`，看到静音视频、目标文本和参考语音三项输入。
2. 播放自动导览，或点击任一输入接管交互。
3. 切换 Scene、Face、Lip，查看视频提供的不同约束。
4. 拖动时间游标，观察视频帧、音素、韵律和输出同步变化。
5. 切换 Generated Speech 与 Dubbed Video，理解研究输出和产品输出。
6. 点击“Explore methods”，进入方法图谱。

完成条件：用户能够用自己的话准确复述任务输入、输出和主要难点。

## Workflow B：学生或研究者探索一套方法

1. 在 `/methods` 选择 HPMDubbing、StyleDubber 或 EmoDubber。
2. 阅读该方法的一句话问题定义，不先展开所有技术细节。
3. 点击 Method Canvas 中的一个组件。
4. 检查组件输入、输出、论文章节和对应时序信号。
5. 固定该信号，再点击下一组件观察数据如何变化。
6. 切换 Overview、Flow、Signals、Evidence、Reproduce。
7. 打开 Paper、Source 或 Cite。

完成条件：用户能够说明该方法的完整主路径，而不是只记住一个模型名称。

## Workflow C：评审比较三项团队成果

1. 从 Atlas 的研究演进线依次查看三套方法。
2. 保持相同案例和时间位置。
3. 进入 Comparison Lab。
4. 开启盲听模式，依次播放 Candidate A/B/C。
5. 查看共同适用的同步、音色、情感或清晰度证据。
6. 提交当前案例偏好，再揭示方法名称。
7. 导出带方法版本和素材来源的比较摘要。

完成条件：比较结论限定在当前案例和可用证据范围内。

## Workflow D：创作者根据需求选择方法

1. 选择一个已授权的 Replay 或本地项目案例。
2. 指定主要需求：口型与韵律、风格保持、显式情感控制。
3. 系统只筛选满足输入和控制要求的方法。
4. 用户查看方法说明和已有结果，不接受无证据的自动全局排名。
5. 如果某方法处于 Live 且环境就绪，进入 Studio 生成候选。
6. 如果只有 Replay，用户仍可完成理解和比较，但不能修改输入后声称重新生成。

完成条件：用户清楚知道选择依据、方法状态和当前结果来源。

## Workflow E：开发者制作 Replay Bundle

1. 准备自制、公共领域或获得明确许可的视频和参考语音。
2. 使用固定 commit、权重哈希和参数执行方法。
3. 导出目标语音、配音视频和允许公开的中间产物。
4. 运行 `opendub atlas pack` 生成 bundle manifest 和资源哈希。
5. 运行 Schema、时间轴、媒体探测和权利清单校验。
6. 在本地 Atlas 预览并检查所有状态标签。
7. 提交内容 PR，不把原始受限素材或未知许可权重放入仓库。

完成条件：离线浏览器能够回放 bundle，Evidence Room 能追溯来源。

## Workflow F：开发者接入 Live 完整方法

1. 审计源码、依赖、权重和数据限制。
2. 实现完整方法 Adapter，不调用其他论文方法内部模块。
3. 实现 `VisualizationProvider`，将允许导出的中间产物映射到 Atlas 信号契约。
4. 使用授权 fixture 完成真实烟雾测试。
5. 对照 Concept Canvas 检查 Live 信号命名和时间单位。
6. 更新方法 manifest，从 Planned 或 Replay 升级到 Live。
7. 更新模型卡、复现命令、限制、测试和 Evidence Room。

完成条件：真实运行可复现，失败时不会自动回退为未标记的 Replay。

## Workflow G：申报视频录制

1. 固定发布 commit、浏览器版本、视口和案例。
2. 运行演示预检，确认所有媒体、字体和 Replay Bundle 本地可用。
3. 从 Task Explorer 录制任务定义。
4. 依次录制三个 Method Canvas 的核心交互。
5. 录制同输入 A/B/C 比较。
6. 只有在真实适配器就绪时录制 Live；否则明确展示 Replay。
7. 录制 Evidence Room 和开源仓库。
8. 按事实核验表审查每个旁白句子和画面标签。

完成条件：影片中不存在状态混淆、未授权素材或无法在发布版本中复现的功能。
