# OpenDub

> **OpenDub: An Open-Source Platform for Multimodal Intelligent Video Dubbing**<br>
> **OpenDub：面向 AIGC 内容生产的多模态智能视频配音开源平台**

> *Interactive Method Atlas, Visual Comparison, and Complete-Method Workbench.*

OpenDub explains the video dubbing task as a synchronized transformation:

```text
Video + Target Text + Authorized Reference Speech
                    │
                    ▼
            one complete dubbing method
                    │
                    ▼
          Target Dubbed Speech -> Dubbed Video
```

It is an open-source, local-first platform for understanding the task, selecting an appropriate complete method, preparing authorized inputs, inspecting method evidence, and conditionally comparing or running a method when the evidence permits. Rather than presenting a gallery of papers or combining incompatible internal modules into a new unverified model, OpenDub keeps each research method intact and builds a shared explanation, evidence, and preparation layer around it.

## Method Atlas

The first public Concept release focuses on three related but independent research foundations:

| Method | Research focus | Atlas status |
|---|---|---|
| [HPMDubbing](https://github.com/GalaxyCong/HPMDubbing) | Hierarchical visual prosody from lip motion, face affect, and scene context | `Concept` |
| [StyleDubber](https://github.com/GalaxyCong/StyleDubber) | Phoneme-level and utterance-level multi-scale style learning | `Concept` |
| [EmoDubber](https://github.com/GalaxyCong/EmoDubber) | Lip-aware synchronization, pronunciation, identity, and emotion-guided dubbing | `Concept` |

Each method is pinned to an upstream source commit and described by a validated Method Manifest. The interactive web atlas contains:

- **Task Explorer**: distinguishes the research output, target speech, from the product output, a muxed dubbed video.
- **Method Atlas and Canvas**: lets a viewer trace complete method-specific paths and inspect evidence-bound components and signals.
- **Comparison Lab**: permits rankings only when methods share exactly the same video, text, reference speech, rights record, and timing policy.
- **Studio**: turns an Atlas selection into a local project, records authorized inputs, and exports a versioned preparation manifest for the selected complete method.

The platform never represents Concept illustrations as model output. `Replay` requires an authorized result bundle; `Live` requires a verified checkpoint, isolated runtime, and real smoke test.

## Project Status

OpenDub is under active development. The current application release is `v0.0.1-alpha.0`; its verified scope, known limits, and next evidence gates are recorded in [Project Current State](docs/PROJECT_CURRENT_STATE.md).

The verified application-release path is:

1. explain the multimodal task in Task Explorer;
2. inspect one of three complete Concept methods and its evidence;
3. persist an evidence-bound method selection in a local Studio project;
4. record the selected method's authorized video, text, and reference-speech inputs;
5. export a versioned preparation manifest without claiming a fresh model output.

Model integrations are only marked as supported after source, weights, license, and real inference verification. See [the upstream baseline](TODO/01_CAPABILITIES/UPSTREAM_BASELINE.md) for the current evidence boundary.

## Research Foundations

OpenDub is designed around the team's prior open work in movie dubbing. HPMDubbing, StyleDubber, and EmoDubber are the three complete core methods in the first Method Atlas. HPMDubbing_Vocoder is supporting acoustic infrastructure, not a fourth method. None are automatically production backends: their source, weights, runtime, asset rights, and result provenance are reviewed independently.

## Validate The Atlas

The public method manifests are versioned data, not hand-written UI text:

```bash
.venv/bin/opendub atlas validate --content content
```

The command validates all nodes, edges, signals, fixed source commits, and method graph references. The current checkpoint availability audit is documented in [docs/atlas/checkpoint-audit-2026-07-26.md](docs/atlas/checkpoint-audit-2026-07-26.md); accessible Drive files remain candidates until their hashes, terms, runtime, and authorized fixtures are independently recorded.

For a plain-language overview of the current project, implemented pages, evidence boundary, recording route, and next steps, see [Project Current State](docs/PROJECT_CURRENT_STATE.md). The platform-level workflow is shown in the editable [architecture figure](docs/architecture/README.md).

## Responsible Use

Only process video, scripts, and voice references that you own or are authorized to use. Do not impersonate people, mislead audiences, or distribute restricted media. OpenDub is designed to run locally by default and does not upload user media for telemetry.

## Documentation

- [Local Alpha Quick Start](docs/getting-started/local-alpha.md)
- [Model Admission Status](docs/adapters/model-status.md)
- [Grant project summary](docs/grant/project-summary.md) and [evidence index](docs/grant/evidence-index.md)
- [Application video delivery](docs/grant/video/README.md), [subtitle source](docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0_CN_EN.srt), and [recording script](docs/grant/demo-script.md)
- [Release history](CHANGELOG.md)
- The detailed engineering, product, release, grant, and formal-film plans remain in [TODO/README.md](TODO/README.md).

## Local Containers

The optional compose stack keeps both services on loopback addresses and stores project data in a
named local Docker volume. It contains no model weights.

```bash
docker compose up --build
```

Open the Studio at `http://127.0.0.1:8080`. The API is available at
`http://127.0.0.1:8000/api/docs`.

## Redistributable Examples

Build two synthetic, no-model alpha projects with FFmpeg test media:

```bash
uv run python scripts/build_examples.py --workspace /tmp/opendub-examples
```

See [examples/ASSET_LICENSES.md](examples/ASSET_LICENSES.md) for the media policy. These examples
exercise the current project, authorization, and timeline workflow; they do not provide real
dubbing output.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security issues must be reported through [SECURITY.md](SECURITY.md), not public issues.

## License

New OpenDub platform code is licensed under [Apache-2.0](LICENSE). Model adapters, upstream source code, weights, datasets, and example media may carry separate terms; see [NOTICE](NOTICE).
