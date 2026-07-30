# Changelog

All notable OpenDub platform changes are recorded here. Version labels describe the platform and evidence layer; they do not imply that an upstream research method has passed the OpenDub `Live` admission gate.

## v0.4.0-showcase - 2026-07-30

### Added

- Final V4.6 project introduction film with bilingual subtitles, checksum, and a public showcase delivery record.
- A public repository landing page centered on the video-dubbing task, team-developed complete methods, authorized archived examples, and the interactive OpenDub experience.
- Direct GitHub playback links for the authorized Case 03 and Case 04 archived examples, with their method identity, manifests, and rights records kept visible.
- A curated public documentation index and project overview.

### Changed

- Moved submission material, review rounds, historical plans, earlier proposal-film assets, narration experiments, capture intermediates, and production-only scripts into a local ignored archive.
- Updated project metadata and citation information for the `wsincos/OpenDub` public repository.

## v2.0.0-showcase - 2026-07-27

### Added

- VTTS Task Stage as the default route: an interactive, controllable explanation of `Video + Target Text + Authorized Reference Speech -> Complete Method -> Target Speech + Dubbed Video`.
- Face, Lip, and Environment inspection layers plus GT-audio-derived waveform, F0, energy, and log-mel displays. The visible IPA is explicitly task notation, not a transcription of the archived cases.
- Two manifest-bound historical example families (`human-0` and `animation-1`) with GT, HPMDubbing, StyleDubber, and EmoDubber media panels, source hashes, feature provenance, a public-scope authorization record, and one-track playback coordination.
- An 84.203-second V2 caption-led film with actual browser-recorded task interactions, explicit non-speech explanation audio, labeled GT sample audio, embedded Chinese/English subtitles, build script, delivery manifest, and SHA-256 verification.
- Case-bundle verification that checks source media, public copies, derived features, provenance hashes, authorization record, and Replay claim boundaries.
- A controlled source-evidence register for the restricted historical inputs, with per-artifact hash anchors, permitted display scope, maintainer verification contact, and withdrawal handling.

### Deliberate limitations

- The V2 cases remain `Archived research example`; they do not have canonical transcript / IPA or same-input Replay contracts and are never shown as a fair ranking, `Replay`, `Live`, or fresh OpenDub output.
- The V2 film does not show the Studio network/API screen. It does not promote preparation export as a demonstrated V2 video capability.

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
