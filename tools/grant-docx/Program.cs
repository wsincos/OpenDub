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

        SetCell(rows[2], 1, "OpenDub：面向视频内容创作的本地优先智能配音开源工具", 10);
        SetCell(rows[3], 1, "https://github.com/GalaxyCong/OpenDub", 9);
        SetCell(rows[3], 3, "Apache License 2.0；上游模型代码、权重与数据遵循各自许可", 9);
        SetCell(rows[4], 3, "v0.0.1-alpha.0", 10);
        SetCell(rows[8], 1, "视频配音同时受文本、人物音色、口型与表情节奏、场景和目标时长约束。现有开源研究代码多以训练和离线评测为中心，输入格式、环境和指标分散，创作者难以从授权素材走到可追溯的配音结果。OpenDub 面向这一断裂，建设本地优先的统一工作流，并把声音授权、版本控制和运行记录纳入默认流程。", 9);
        SetCell(rows[9], 1, "当前 Alpha 已实现：本地项目与微秒时间线、FFmpeg 媒体基础、内容寻址素材存储、授权参考声音、模型审计注册表、运行清单/基础指标、CLI/API 和 Web Studio 的项目创建、媒体导入、授权登记、片段配置与时间线展示。真实视频感知模型、真实情感控制、候选 A/B、完整评测与成片导出属于后续验收目标。", 9);
        SetCell(rows[10], 1, "项目与时间线层（project.json 真相源、revision、微秒时间）；媒体层（FFprobe/FFmpeg、字幕、音频和渲染）；授权与素材层（SHA-256、素材—授权—参考声音关联）；模型层（能力合同、固定 commit、隔离运行时）；生成/评测层（候选、run.json、基础指标）；服务层（FastAPI、CLI、React Studio）。", 9);
        SetCell(rows[11], 1, "1. 统一视频、台词、授权声音、情感方向和目标时间窗的数据合同；2. 以能力声明、许可/权重审计和真实烟雾测试控制模型准入；3. 默认记录授权、内容哈希、revision 和运行清单；4. 将视频韵律、情感、风格和声学渲染组织为可替换的开源能力后端。", 9);
        SetCell(rows[12], 1, "团队已有 HPMDubbing、StyleDubber、EmoDubber、HPMDubbing_Vocoder 等视频配音研究与开源技术基础。OpenDub 不直接拼接原仓库，而是公开统一 Schema、适配接口、上游审计和可追溯工作流。申报提交前应从公开主页实时补充 Stars、Issue、版本发布和外部贡献等数据。", 9);
        SetCell(rows[13], 1, "当前自动化验证环境：Linux、Python 3.13、FFmpeg、现代 Chromium 浏览器；项目元数据声明 Python >=3.11,<3.14。GPU、CUDA、国产硬件、Docker GPU 与真实模型权重尚未完成受控验证，不写为已支持。", 9);
        SetCell(rows[15], 1, "README、项目规划和申报底稿：github.com/GalaxyCong/OpenDub；本地 API 文档：启动服务后访问 /api/docs。正式发布前补充中英文快速开始、模型卡、Adapter 教程和可再分发示例。", 9);
        SetCell(rows[16], 1, "申报 Alpha 演示视频待按仓库 docs/grant/demo-script.md 录制；正式 2 分 40 秒影片须在真实模型、候选、评测和导出证据齐备后按 TODO/04_OPEN_SOURCE/DEMO_FILM 制作。", 9);
        SetCell(rows[18], 1, "M1 可信项目闭环：主仓库、Schema、媒体、授权、Web Studio Alpha。\nM2 真实模型闭环：首个经许可和真实烟雾验证的后端/声码器、候选、评测、WAV/MP4。\nM3 开源发布：Docker、CI、两套授权示例、中英文文档、Adapter 教程、v0.1.0 和社区共建。", 9);
        SetCell(rows[19], 1, "核心工具持续开源。项目成熟后可面向内容团队提供可选的私有部署、模型适配、推理优化和工作流集成服务；不以采集用户素材、出售未授权声音或封闭 SaaS 为短期目标。", 9);
        SetCell(rows[20], 1, "在权重许可与真实验证条件满足后，依次接入视频韵律、情感、风格与声学渲染后端，完善候选比较、内容/音色/情感/同步评测、长视频与多角色流程；GPU、国产硬件和多语言能力均以实测结果为准。", 9);
        SetCell(rows[21], 1, "希望获得受控 GPU 算力和真实模型验证环境、开源许可证/权重合规指导、授权内容创作场景试用、开发者社区传播与外部 Adapter 共建资源，以及后续国产算力验证支持。", 9);
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

static void SetCell(TableRow row, int cellIndex, string content, int points)
{
    var cell = row.Elements<TableCell>().ElementAt(cellIndex);
    var properties = cell.GetFirstChild<TableCellProperties>()?.CloneNode(true) as TableCellProperties;
    cell.RemoveAllChildren();
    if (properties is not null) cell.Append(properties);

    var paragraph = new Paragraph(
        new ParagraphProperties(new SpacingBetweenLines { After = "0", Line = "240", LineRule = LineSpacingRuleValues.Auto }));
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
