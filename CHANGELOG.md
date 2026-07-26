# Changelog

All notable OpenDub platform changes are recorded here. Version labels describe the platform and evidence layer; they do not imply that an upstream research method has passed the OpenDub `Live` admission gate.

## v0.0.1-alpha.0 - 2026-07-26

### Added

- Interactive Task Explorer for `Video + Target Text + Authorized Reference Speech -> Complete Method -> Target Speech -> Dubbed Video`.
- Method Atlas and click-through Canvases for the complete HPMDubbing, StyleDubber, and EmoDubber research methods.
- Explainable first-need guidance: visual prosody / scene rhythm, pronunciation / character style, and explicit emotion direction.
- Evidence-bound method selection, local Studio preparation workflow, authorization checks, and `opendub.project-preparation/v1` export.
- Evidence Room, common-input comparison rules, fixed upstream source revisions, and model admission criteria.
- Architecture source and SVG, completed application form, and a 110-second bilingual-subtitle application walkthrough with SHA-256 delivery record.
- CI quality gate covering Python format/lint/type/tests, Web type checks/component tests/production build, and Markdown link validation.

### Deliberate limitations

- HPMDubbing, StyleDubber, and EmoDubber are public `Concept` methods in this release, not admitted `Live` runtimes.
- There is no qualified same-input `Replay` bundle, so the Comparison Lab shows no audio, metric, or ranking result.
- The walkthrough narration explains the platform only; it is not an OpenDub or upstream-method generated dubbing sample.
