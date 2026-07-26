# OpenDub V2 Showcase Video

`OpenDub_VTTS_Showcase_v2.0.0.mp4` is the V2 application-demo delivery. It is separate from the V1 film and focuses on the VTTS task, real archived examples, complete-method visualization, and evidence boundaries.

## Delivery

| Item | Value |
| --- | --- |
| Duration | 84.203 seconds |
| Picture | 1920x1080, H.264, 30 FPS |
| Audio | AAC, 48 kHz stereo; task segments use labeled non-speech explanation audio, sample segments use the marked GT track |
| Subtitles | embedded `mov_text` plus [SRT](OpenDub_VTTS_Showcase_v2.0.0_CN_EN.srt) |
| Narration | [Chinese recording script](narration.zh-CN.md) |
| Fact boundary | [fact-check.md](fact-check.md) |
| File hashes | [delivery-manifest.json](delivery-manifest.json) and `OpenDub_VTTS_Showcase_v2.0.0.sha256` |

The film is caption-led so the visual task explanation and real sample audio can be checked without presenting a synthetic narrator as a model result. Its first 20 seconds are actual browser recordings of the task flow, cue switching, and timeline dragging; they use an in-frame-labeled non-speech explanation track. The Chinese narration script remains available for a human recording pass; do not replace the labeled GT segments with an unmarked voice-over.

## What The Film Shows

1. `/vtts`: `Video + Target Text + Authorized Reference Speech -> Complete Method -> Target Speech + Dubbed Video`.
2. The Face, Lip, Environment, IPA, F0, energy, and real waveform views on a common timebase.
3. `human-0` and `animation-1`: GT, HPMDubbing, StyleDubber, and EmoDubber as `Archived research example` panels, not an unverified benchmark.
4. The three complete methods, an EmoDubber method canvas, and Evidence Room.

## Rebuild

1. Start the web application on a clean local port: `npm --prefix apps/web run dev -- --port 5181`.
2. Regenerate the eight stills under `assets/screens/` with the 1920x1080 URLs used in [the V2 plan](../../../../TODO/07_V2_SHOWCASE/04_FILM_V2_PRODUCTION_PLAN.md), then capture the three true interaction clips:

   ```bash
   node_modules/.bin/playwright install ffmpeg
   node scripts/capture_v2_web_clips.mjs
   ```
3. Verify the two cases and rebuild their features before capture:

   ```bash
   .venv/bin/python scripts/build_showcase_features.py \
     --case content/showcases/v2/human-0.json \
     --output apps/web/public/showcases/v2/human-0
   .venv/bin/python scripts/build_showcase_features.py \
     --case content/showcases/v2/animation-1.json \
     --output apps/web/public/showcases/v2/animation-1
   ```

4. Build the film and its contact sheet:

   ```bash
   bash scripts/build_v2_showcase_film.sh
   ```

5. Run `ffprobe`, inspect `contact-sheet.png`, listen to the non-speech task bed and both archived-case segments, and re-check [fact-check.md](fact-check.md) before publishing. The builder refreshes `delivery-manifest.json` and the MP4 SHA-256 after every successful rebuild.

To audit an already-built public case without rewriting any media, use:

```bash
.venv/bin/python scripts/build_showcase_features.py --verify-only \
  --case content/showcases/v2/human-0.json --output apps/web/public/showcases/v2/human-0
```
