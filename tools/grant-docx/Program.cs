using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Validation;
using DocumentFormat.OpenXml.Wordprocessing;

if (args.Length == 1)
{
    Inspect(args[0]);
    return 0;
}

if (args.Length == 2)
{
    Fill(args[0], args[1]);
    return 0;
}

Console.Error.WriteLine("Usage: GrantDocx <template.docx> [output.docx]");
return 2;

static void Inspect(string path)
{
    using var document = WordprocessingDocument.Open(path, false);
    var tables = document.MainDocumentPart?.Document.Body?.Elements<Table>() ?? [];
    Console.WriteLine($"Tables: {tables.Count()}");
    foreach (var (table, tableIndex) in tables.Select((table, index) => (table, index)))
    {
        Console.WriteLine($"TABLE {tableIndex}");
        foreach (var (row, rowIndex) in table.Elements<TableRow>().Select((row, index) => (row, index)))
        {
            var cells = row.Elements<TableCell>().Select(cell => cell.InnerText.Trim().Replace("\r", " ").Replace("\n", " "));
            Console.WriteLine($"{rowIndex}: {string.Join(" || ", cells)}");
        }
    }
}

static void Fill(string templatePath, string outputPath)
{
    Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(outputPath))!);
    File.Copy(templatePath, outputPath, true);
    using (var document = WordprocessingDocument.Open(outputPath, true))
    {
        var table = document.MainDocumentPart?.Document.Body?.Elements<Table>().SingleOrDefault()
            ?? throw new InvalidOperationException("The template must contain exactly one application table.");
        var rows = table.Elements<TableRow>().ToList();

        SetCell(rows[2], 1, "OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台", 9);
        SetCell(rows[3], 1, "https://github.com/wsincos/OpenDub", 9);
        SetCell(rows[3], 3, "Apache License 2.0；上游代码、权重、数据遵循各自许可", 9);
        SetCell(rows[4], 3, "v0.0.1-alpha.0", 10);
        SetCell(rows[8], 1, "视频配音生成以视频、目标台词和经授权的参考语音为输入，经一套完整配音方法生成目标语音，再与视频混流形成配音视频。它不仅回答“文字怎么念”，还要解释角色在画面、时刻、口型、情绪和场景约束下应怎样说话。已有研究多以论文、训练脚本和独立仓库存在，创作者难以理解方法差异，开发者也难以在同一权利和输入条件下复现比较。OpenDub 围绕这一问题建设可交互、可选择、可准备、可核查的开源平台。", 9);
        SetCell(rows[9], 1, "已完成任务输入/输出解释器，HPMDubbing、StyleDubber、EmoDubber 三套完整方法的可点击图谱和专属交互视图，以及 Evidence Room 和证据门控的 Comparison Lab。Atlas 以“视觉韵律与场景节奏 / 发音清晰度与角色风格 / 显式情感方向”提供可解释的首要需求导览，只建议优先理解和准备的方法，不宣称全局最优。用户选择后平台保存方法 ID、固定证据版本、输入要求、可选控制项和状态；Studio 支持本地项目、媒体导入、参考语音授权、片段时间线、视频/文本确认和版本化 preparation manifest 导出。当前不将 Concept 交互或准备记录表述为真实模型生成结果。", 9);
        SetCell(rows[10], 1, "Atlas 层以结构化 Method Manifest 定义完整方法的节点、边、信号、输入与证据；React 前端以 Task Explorer、Method Atlas、Evidence Room 和 Studio 提供交互。项目层以版本化 project.json、整数微秒时间线和 SHA-256 素材记录为真相源；准备导出层校验视频哈希、文本指纹、参考语音同意和方法一致性。FastAPI、CLI、FFmpeg/FFprobe、模型注册表与隔离 Adapter 为后续通过准入的完整方法提供本地工作流。", 9);
        SetCell(rows[11], 1, "1. 将视频、文本、经授权参考语音和目标配音/成片输出组织为可交互理解的多模态任务；2. 保留 HPMDubbing、StyleDubber、EmoDubber 三套完整方法，不将不同论文内部模块拼成未经验证的新模型；3. 用 Method Manifest、固定证据版本和可点击图谱把方法机制、来源、限制与用户选择关联；4. 用 Concept、Replay、Live、Planned 严格区分机制说明、历史结果和真实运行，并把输入权利与可复现准备记录纳入默认流程。", 9);
        SetCell(rows[12], 1, "团队已有 HPMDubbing、StyleDubber、EmoDubber 和 HPMDubbing_Vocoder 等视频配音研究与开源技术基础。OpenDub 的新增贡献是将完整方法组织为统一、可交互、可审计、可选择的开放工作台，公开方法描述、固定上游源码版本、许可证/权重审计、选择记录、准备清单和后续 Adapter 准入接口；不将上游工作简单并列或误写为已内置 Live 后端。", 9);
        SetCell(rows[13], 1, "已在 Linux、Python 3.13、FFmpeg 和现代 Chromium 环境完成自动化验证；项目元数据支持 Python >=3.11,<3.14。当前 Web 端覆盖桌面和移动端；GPU、CUDA、国产硬件、Docker GPU、真实模型权重及浏览器视频格式尚未完成受控验证，后续以实测结果为准。", 9);
        SetCell(rows[15], 1, "仓库已提供 README、项目说明、平台架构图（draw.io/SVG）、快速开始、方法审计、Method Manifest、申报摘要/证据索引、演示视频及中英字幕/校验和、演示脚本和完整 TODO 规划；统一入口：https://github.com/wsincos/OpenDub。启动本地服务后可访问 /api/docs；后续补充中英文模型卡、Adapter 教程和可再分发示例。", 8);
        SetCell(rows[16], 1, "已交付 110 秒申报视频：解释 Video + Target Text + Authorized Reference Speech -> Complete Method -> Target Speech -> Dubbed Video；展示按需求选择、可点击组件、Studio 授权准备和 Evidence Room。附件：docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4（含中英字幕、SHA-256 和事实边界清单）。旁白非模型输出，未伪造生成、A/B 结果或指标。", 8);
        SetCell(rows[18], 1, "M1（已完成 Alpha）：任务解释器、三方法 Concept Atlas、证据边界、方法选择、Web Studio 本地授权项目和 preparation manifest 导出。\nM2（已完成申报冻结）：平台架构图、统一文档/申报材料、质量验证、110 秒演示视频和可引用发布版本。\nM3（条件升级）：在权重许可、授权素材和真实 smoke test 齐备后，接入首个完整后端与声码器，形成真实 Replay、候选比较、基础评测和 WAV/MP4 导出；再发布 v0.1.0 与社区共建机制。", 9);
        SetCell(rows[19], 1, "核心平台持续开源。项目成熟后，可面向内容团队提供可选的私有部署、完整方法适配、推理优化、生产工作流集成和技术支持；不以采集用户素材、出售未授权声音或封闭 SaaS 为短期目标。", 9);
        SetCell(rows[20], 1, "在明确代码/权重许可、SHA-256、授权样例、隔离环境和真实 smoke test 后，按完整方法逐一接入视频韵律、风格和情感配音后端；建设同输入 Replay、候选 A/B/C 比较、内容/音色/情感/同步评测、长视频与多角色工作流。GPU、国产硬件、多语言和实时能力均以公开测试报告为准。", 9);
        SetCell(rows[21], 1, "希望获得受控 GPU 算力和真实模型验证环境；开源许可证、模型权重与数据合规指导；公开课、动画、数字人等已授权内容创作场景的试用反馈；开发者社区传播、外部完整方法 Adapter 共建和国产算力验证资源。", 9);
        CompactTrailingNotice(document.MainDocumentPart?.Document.Body, table);
        document.MainDocumentPart?.Document.Save();
    }

    using var validationDocument = WordprocessingDocument.Open(outputPath, false);
    var errors = new OpenXmlValidator(FileFormatVersions.Office2013).Validate(validationDocument).ToList();
    if (errors.Count != 0)
    {
        throw new InvalidOperationException($"OpenXML validation failed: {string.Join("; ", errors.Take(3).Select(error => error.Description))}");
    }
    Console.WriteLine($"Wrote and validated {outputPath}");
}

static void CompactTrailingNotice(Body? body, Table table)
{
    if (body is null) return;

    // The supplied template has an empty paragraph before its fixed upload note.
    // Removing only that empty spacer and compacting the note prevents a one-line third page.
    var followingParagraphs = table.ElementsAfter().OfType<Paragraph>().ToList();
    var spacer = followingParagraphs.FirstOrDefault(paragraph => string.IsNullOrWhiteSpace(paragraph.InnerText));
    spacer?.Remove();

    var notice = followingParagraphs.FirstOrDefault(paragraph => paragraph.InnerText.TrimStart().StartsWith("注：", StringComparison.Ordinal));
    if (notice is null) return;

    var properties = notice.GetFirstChild<ParagraphProperties>();
    if (properties is null)
    {
        properties = new ParagraphProperties();
        notice.PrependChild(properties);
    }
    properties.SpacingBetweenLines = new SpacingBetweenLines
    {
        Before = "0",
        After = "0",
        Line = "220",
        LineRule = LineSpacingRuleValues.Auto,
    };
    properties.SnapToGrid = new SnapToGrid { Val = false };

    foreach (var run in notice.Descendants<Run>())
    {
        var runProperties = run.GetFirstChild<RunProperties>();
        if (runProperties is null)
        {
            runProperties = new RunProperties();
            run.PrependChild(runProperties);
        }
        runProperties.FontSize = new FontSize { Val = "20" };
        runProperties.FontSizeComplexScript = new FontSizeComplexScript { Val = "20" };
    }
}

static void SetCell(TableRow row, int cellIndex, string content, int points)
{
    var cell = row.Elements<TableCell>().ElementAt(cellIndex);
    var properties = cell.GetFirstChild<TableCellProperties>()?.CloneNode(true) as TableCellProperties;
    cell.RemoveAllChildren();
    if (properties is not null) cell.Append(properties);

    var paragraph = new Paragraph(
        new ParagraphProperties(new SpacingBetweenLines { After = "0", Line = "220", LineRule = LineSpacingRuleValues.Auto }));
    var lines = content.Split('\n');
    foreach (var (line, index) in lines.Select((value, position) => (value, position)))
    {
        if (index > 0) paragraph.Append(new Run(new Break()));
        paragraph.Append(new Run(
            new RunProperties(
                new RunFonts { Ascii = "Arial", HighAnsi = "Arial", EastAsia = "Microsoft YaHei" },
                new FontSize { Val = (points * 2).ToString() }),
            new Text(line) { Space = SpaceProcessingModeValues.Preserve }));
    }
    cell.Append(paragraph);
}
