# V3 Release Checklist

Release: `v3.0.0-narrated-evidence`

## Content Boundary

- [x] The female scene is labelled `TASK ILLUSTRATION`; it has no case-audio or transcript claim.
- [x] Its timeline retains English IPA, illustrated pitch/energy, and illustrated target-speech output.
- [x] `human-0` and `animation-1` remain historical research examples, not Live, Replay, fresh OpenDub runs, rankings, or a fair common-input benchmark.
- [x] The three methods are presented as complete methods, not parts combined into a fourth model.

## Audio and Playback Integrity

- [x] Six narration excerpts come only from V1's approved Chinese synthetic-narration stream.
- [x] Narration is absent during the eight historical-example clips.
- [x] Every historical clip has one visible active panel and an `AUDIBLE:` label for its own artifact.
- [x] The source-audio map checks all eight case/artifact pairs, expected labels, matching `a:0` inputs, source existence, and browser capture existence.
- [x] Inactive gallery players pause, reset to zero, and mute when a different artifact starts or the case changes.

## Delivery Integrity

- [x] The V3 MP4 is H.264/AAC with a `mov_text` Chinese-and-English subtitle stream at 1920x1080, 30 FPS, and exactly 112 seconds.
- [x] The delivery manifest records the generated SHA-256, stream facts, repository baseline, source contract, and content boundary.
- [x] The sibling `.sha256` file validates the MP4.
- [x] V1 and V2 delivery paths and tags are not overwritten by V3.

## Required Verification

```bash
.venv/bin/python scripts/verify_v3_audio_map.py docs/grant/video/v3/source-audio-map.json --root . --require-captures
.venv/bin/pytest tests/unit/quality/test_v3_audio_map.py tests/unit/quality/test_v3_capture_inventory.py tests/unit/quality/test_v3_video_manifest.py -v
(cd docs/grant/video/v3 && sha256sum -c OpenDub_Narrated_Evidence_Walkthrough_v3.0.0.sha256)
make check
```
