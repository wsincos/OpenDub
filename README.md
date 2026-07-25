# OpenDub

> **Video-aware, emotion-directed dubbing.**

OpenDub is an open-source, local-first studio for creating video dubbing that respects the scene, character, emotion, and target timing of each line.

Unlike text-to-speech tools that only read a script, OpenDub treats a dubbing project as a synchronized set of video, dialogue, authorized voice references, generation controls, candidate takes, and evaluation records. The project is being built as a reusable open-source workflow for creators, researchers, and model developers.

## Project Status

OpenDub is under active development. The planned first public release is `v0.1.0`; current implementation status is tracked in [TODO/README.md](TODO/README.md).

The first release will focus on:

- local video, script, and authorized voice-reference projects;
- video-aware timing and emotion-directed dubbing adapters;
- candidate comparison, evaluation, and MP4/WAV rendering;
- a Web Studio, REST API, CLI, Docker workflow, and reproducible run manifests.

Model integrations are only marked as supported after source, weights, license, and real inference verification. See [the upstream baseline](TODO/01_CAPABILITIES/UPSTREAM_BASELINE.md) for the current evidence boundary.

## Research Foundations

OpenDub is designed around the team's prior open work in movie dubbing, including HPMDubbing, StyleDubber, EmoDubber, and HPMDubbing_Vocoder. These projects are research foundations and potential adapters; they are not automatically production backends in OpenDub.

## Responsible Use

Only process video, scripts, and voice references that you own or are authorized to use. Do not impersonate people, mislead audiences, or distribute restricted media. OpenDub is designed to run locally by default and does not upload user media for telemetry.

## Documentation

- [Local Alpha Quick Start](docs/getting-started/local-alpha.md)
- [Model Admission Status](docs/adapters/model-status.md)
- [Grant project summary](docs/grant/project-summary.md) and [evidence index](docs/grant/evidence-index.md)
- [Alpha demo recording script](docs/grant/demo-script.md)
- The detailed engineering, product, release, grant, and formal-film plans remain in [TODO/README.md](TODO/README.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security issues must be reported through [SECURITY.md](SECURITY.md), not public issues.

## License

New OpenDub platform code is licensed under [Apache-2.0](LICENSE). Model adapters, upstream source code, weights, datasets, and example media may carry separate terms; see [NOTICE](NOTICE).
