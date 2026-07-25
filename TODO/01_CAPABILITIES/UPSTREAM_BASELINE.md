# Upstream Baseline

## 快照时间与用途

本快照基于 2026 年 7 月 25 日可公开访问的 GalaxyCong GitHub 页面和仓库 README。它用于规划与申报证据，不替代正式的 commit、许可证和权重审计。Stars、commit 和仓库内容会变化，填写申报表前需再次核验。

## 公开资产

### EmoDubber

- URL：`https://github.com/GalaxyCong/EmoDubber`
- 定位：CVPR 2025 高质量、情感可控电影配音。
- 公开状态：Python、MIT、约 43 commits、38 Stars。
- 已公开说明：基本训练/推理和基础权重可用。
- 关键限制：README 的情感控制代码和若干评测脚本仍标为未完成；训练说明包含手工替换 Lightning 安装文件的步骤。
- OpenDub 结论：首选 Adapter，但必须先验证情感控制的真实可发布实现；不能仅根据论文标题标为 Stable。

### HPMDubbing

- URL：`https://github.com/GalaxyCong/HPMDubbing`
- 定位：CVPR 2023，利用口型、面部表情和场景信息进行分层韵律建模。
- 公开状态：Python、MIT、约 110 commits、112 Stars。
- 已公开说明：模型、预处理、数据特征、推理和演示较完整。
- 关键限制：流程存在旧环境、硬编码路径和复杂手工预处理；部分影视数据受版权限制。
- OpenDub 结论：作为首版三套完整 Method Canvas 之一。其 Lip、Face、Scene 分层结构用于任务解释与可视化；真实 Live 适配仍需独立准入。

### StyleDubber

- URL：`https://github.com/GalaxyCong/StyleDubber`
- 定位：ACL 2024，多尺度风格学习电影配音。
- 公开状态：Python、MIT、约 58 commits、98 Stars。
- 已公开说明：训练/推理、权重、数据特征和部分指标。
- 关键限制：环境基于 Python 3.8/CUDA 11.5，模型输入与数据配置偏研究复现。
- OpenDub 结论：作为首版三套完整 Method Canvas 之一。其 MPA、PLA、USL 用于方法解释与可视化；真实 Live 适配必须在独立环境中完成。

### HPMDubbing_Vocoder

- URL：`https://github.com/GalaxyCong/HPMDubbing_Vocoder`
- 定位：HPMDubbing 使用的 HiFi-GAN 波形生成。
- 公开状态：Python、MIT、约 28 commits、18 Stars。
- 已公开说明：16kHz 和 22050Hz 路径、预训练模型与 mel-to-wave 推理。
- 关键限制：不同采样率配置具有不同 hop length、窗口和参数，必须严格匹配声学模型。
- OpenDub 结论：适合作为独立 VocoderAdapter，先完成 mel 契约与权重哈希核验。

### HD-Dub

- URL：`https://github.com/GalaxyCong/HD-Dub`
- 当前代码地址：`https://github.com/HD-Dub/HDCode`
- 定位：层次音素建模与声学扩散去噪。
- 公开状态：GalaxyCong 仓库主要用于迁移指引；HDCode 固定 commit 为
  `d08839848cf17805bb598abf468968f8fc7a28f7`，根目录为 MIT，包含训练与推理入口。
- 已知契约：README 将数据/特征声明为 22050 Hz，并分别列出 CHEM、GRID、V2C-Animation
  的训练和推理命令。
- 关键限制：README 明确将预处理特征和三个 checkpoint 标记为“待上传”；HiFi-GAN 链接未提供
  可审计的权重条款、版本或 SHA-256，且未完成隔离环境真实推理。
- OpenDub 结论：Planned，不进入首版承诺；详见 `docs/audits/hdcode-d088398.md`。

### CoSyncDiT

- URL：`https://github.com/GalaxyCong/CoSyncDiT`
- 定位：ECCV 2026 Cognitive Synchronous Diffusion Transformer。
- 公开状态：当前仅 README，约 1 commit，未见公开代码、许可证和权重。
- OpenDub 结论：Planned；代码与权重正式发布后才能设计 Adapter。

### LLM-Flow-Dubber

- URL：`https://github.com/GalaxyCong/LLM-Flow-Dubber`
- 公开状态：HTML/CSS 演示页面，约 2 commits，未见模型代码和明确许可证。
- OpenDub 结论：作为上下文/指令控制方向的研究证据，不能作为当前可调用模型。

### EmoDub

- URL：`https://github.com/GalaxyCong/EmoDub`
- 公开状态：静态 HTML 演示，包含图像和视频。
- OpenDub 结论：可作为 EmoDubber 研究 Demo 的来源；迁移任何媒体前必须确认素材再分发权。

### HPMDubbing-how-to-get-face-and-lip-

- URL：`https://github.com/GalaxyCong/HPMDubbing-how-to-get-face-and-lip-`
- 定位：脸部与口型预处理补充步骤。
- OpenDub 结论：作为 Vision preprocessing 参考，将手工流程重构为缓存化、可测试组件。

### More-Details-about-the-V2C-Animation-dataset.

- URL：`https://github.com/GalaxyCong/More-Details-about-the-V2C-Animation-dataset.`
- 定位：说明 V2C-Animation 数据集挑战。
- OpenDub 结论：仅用于数据说明与引用，不作为自动下载数据源。

### V2C_24KHz

- URL：`https://github.com/GalaxyCong/V2C_24KHz`
- 公开状态：MIT，但内容和数据用途需进一步核验。
- OpenDub 结论：Reference，首版不接入。

### LS-GAN

- URL：`https://github.com/GalaxyCong/LS-GAN`
- 定位：基于语言的图像编辑，与视频配音主线无直接关系。
- OpenDub 结论：排除，不进入产品 Roadmap。

## 规划结论

### 可以立即进入工程审计

- EmoDubber；
- HPMDubbing；
- StyleDubber；
- HPMDubbing_Vocoder。

### 只能作为技术基础或后续方向

- HD-Dub/HDCode；
- CoSyncDiT；
- LLM-Flow-Dubber；
- 各静态 Demo 和数据说明仓库。

### 不能用于官方承诺的证据

- 只有论文标题而没有公开代码/权重；
- 无许可证的演示仓库；
- 无法确认再分发权的电影片段；
- 未经真实运行验证的 README 功能。

## 实现时的更新方式

正式 Task 2 完成后，本快照不删除，而是在主仓库 `licenses/UPSTREAM_AUDIT.md` 建立精确版本：

- 固定 40 位 commit；
- 记录许可证全文；
- 记录权重 URL、条款和 SHA-256；
- 记录实际运行环境与命令；
- 记录 OpenDub patch；
- 将成熟度从 Planned/Experimental/Stable 中择一写入模型注册表。
