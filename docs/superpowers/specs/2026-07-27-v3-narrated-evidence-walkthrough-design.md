# OpenDub V3 Narrated Evidence Walkthrough Design

**Status:** Approved design basis
**Audience:** Youth Open Source Seed Plan reviewers, research users, and future OpenDub contributors
**Supersedes for V3 delivery:** the V2 task-stage presentation and V2 caption-led video only. V2 remains immutable at `v2.0.0-showcase`.

## Goal

Produce a V3 project experience and application film that explains video dubbing clearly, restores the stronger female-scene task illustration, gives every archived result its own visible-and-audible playback state, and uses the already approved Chinese synthetic narration from the V1 delivery.

V3 remains a platform for explaining, inspecting, selecting, and preparing complete dubbing methods. It does not claim fresh model inference, a common-input benchmark, Replay, or Live generation.

## Non-negotiable boundaries

1. The female scene is a **Task illustration**. Its video frames, English IPA, prosody, and output waveform explain time-aligned task constraints only. It is not associated with `human-0`, `animation-1`, a real speaker, or a newly generated output.
2. `human-0` and `animation-1` remain `Archived research example`. They never receive a rank, a score, a common-input claim, Replay status, or Live status.
3. When an archived panel plays, only its own video and embedded audio may advance. The other three panels are paused at time zero and have no audible audio.
4. V1 Chinese narration is platform narration only. It is never labelled as a model output. During archived example playback, narration is absent so the active artifact's audio can be heard without overlap.
5. Every V3 film shot with archived audio includes an in-frame `AUDIBLE: <artifact label>` caption. Every narration shot includes `PLATFORM NARRATION · SYNTHETIC VOICE` in the delivery metadata, not in the product UI.
6. V3 is a new release line. It does not overwrite the V2 files, hash, manifest, or `v2.0.0-showcase` tag.

## Product design

### 1. Keep the V2 task flow

The default `/vtts` route keeps the existing dark task-flow overview:

```text
Silent Video + Target Text + Authorized Reference Speech
                         -> One Complete Method
                         -> Target Speech + Dubbed Video
```

The flow remains an interactive explanation. Its output cards keep `Task illustration · no fresh run`. The method card continues linking to the three complete methods instead of suggesting that parts of HPMDubbing, StyleDubber, and EmoDubber are combined into a fourth model.

### 2. Restore the female-scene task illustration

The V2 Cue Microscope and synchronized timeline are replaced by a compact, light instrument panel based on the proven V1 hierarchy.

| Element | V3 behavior |
| --- | --- |
| Visual asset | `apps/web/public/atlas/demo/scene-v1.png`, labelled `TASK ILLUSTRATION · CONCEPT SCENE` |
| Section heading | `One scene carries several timing cues.` |
| Visual controls | Independent Face and Lip overlay toggles; each control changes only the illustration overlay |
| Video row | Female-scene filmstrip and a single draggable playhead; it is an illustrated timeline, not media playback |
| PHONEMES row | Existing V2 English IPA tokens: `ðə`, `siːn`, `ˈtʃeɪn.dʒɪz`, `haʊ`, `ə`, `laɪn`, `ʃʊd`, `saʊnd` |
| PROSODY row | Current two-curve visual language, explicitly labelled `ILLUSTRATED PITCH + ENERGY` |
| OUTPUT row | Current waveform visual language, explicitly labelled `ILLUSTRATED TARGET SPEECH` |
| Source label | `TASK ILLUSTRATION · NO CASE AUDIO OR TRANSCRIPT` |

The timeline keeps a play/pause control, elapsed-time display, range input, and a shared playhead. It does not start an audio element. This preserves the teaching interaction without creating a false audio/video pairing.

### 3. Example gallery playback contract

The gallery owns one playback controller per active case. Its state is:

```ts
type ActivePlayback = {
  caseId: string;
  artifactPath: string;
  status: "playing" | "paused";
} | null;
```

On a panel's native `play` event, the controller must:

1. pause every registered player except the event source;
2. set every inactive player `currentTime = 0` and `muted = true`;
3. set the active player `muted = false`;
4. update `ActivePlayback` with the active case and artifact path;
5. render only the matching panel with the active border, `PLAYING`, and `AUDIBLE: <artifact label>`.

On a panel's `pause` or `ended` event, the controller retains the selected panel as the inspected artifact but removes the playing treatment. On a case-tab change or page unmount, it pauses and resets every registered player before changing the case.

Panels must retain their native controls for accessibility. Visual highlighter styles must not cover controls or prevent keyboard activation. Inactive panels retain their first frame/poster and a `READY · audio idle` status.

### 4. Sample data and evidence

The eight existing public MP4s remain the only archived media assets:

| Case | Active artifact labels |
| --- | --- |
| `human-0` | Ground truth, HPMDubbing, StyleDubber, EmoDubber |
| `animation-1` | Ground truth, HPMDubbing, StyleDubber, EmoDubber |

The gallery obtains both its video and audio from the same artifact `src`; it does not create a separate GT audio binding. The case manifests, source-evidence register, authorization record, and provenance files remain unchanged except for V3 documentation that references them.

## V3 application-film design

### Delivery identity

The V3 delivery is separate from V1 and V2:

```text
docs/grant/video/v3/OpenDub_VTTS_Narrated_Evidence_v3.0.0.mp4
```

It includes an SRT, delivery manifest, contact sheet, SHA-256, fact-check, source-audio map, browser capture clips, build script, and a short Chinese narration-map document. The final release tag is reserved until all V3 checks and an independent audit score of at least `9 / 10` are complete.

### Audio source contract

V3 reuses the accepted V1 audio track at:

```text
docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4#a:0
```

The build extracts only the following narration ranges. The original video is the authoritative source, and the V3 source-audio map records every extraction range and V1 subtitle reference.

| V3 use | V1 source range | Meaning |
| --- | --- | --- |
| Opening identity | `00:00–00:14` | Platform identity |
| Task definition | `00:14–00:28` | Three inputs, complete method, two outputs |
| Method selection | `00:28–00:50` | HPMDubbing, StyleDubber, EmoDubber as complete methods |
| Method inspection | `00:50–01:07` | Method Canvas and Concept boundary |
| Evidence gate | `01:23–01:38` | No evidence, no Live claim |
| Closing | `01:38–01:50` | No invented comparison and closing statement |

The V3 build normalizes narration segments to an integrated target of `-16 LUFS` with a true peak no higher than `-1 dBTP`. It does not generate a new voice, use voice cloning, or use the narration during archived sample playback.

### Film sequence

The target duration is 100–112 seconds at 1920x1080 and 30 FPS.

| Segment | Target duration | Picture | Audio |
| --- | ---: | --- | --- |
| Identity | 0–14 s | V3 task-stage opening | V1 opening narration |
| Task illustration | 14–28 s | real browser capture of V3 task flow, female Face/Lip panel, and illustrated timeline | V1 task-definition narration |
| Human examples | 28–37 s | four real browser captures: GT, HPMDubbing, StyleDubber, EmoDubber, one active panel at a time | each active `human-0` artifact's own audio, 2.25 s each |
| Animated examples | 37–46 s | four real browser captures: GT, HPMDubbing, StyleDubber, EmoDubber, one active panel at a time | each active `animation-1` artifact's own audio, 2.25 s each |
| Complete methods | 46–68 s | method selection and the three method entries | V1 method-selection narration |
| Method inspection | 68–85 s | interactive Method Canvas capture | V1 method-inspection narration |
| Evidence boundary | 85–100 s | Evidence Room capture and status labels | V1 evidence-gate narration |
| Close | 100–112 s | return to V3 task flow and project identity | V1 closing narration |

The exact browser clip duration can differ by less than one second only when media durations require it; the source-audio map and SRT must be regenerated from the final timeline. Sample clips never overlap each other, and their final frame visibly identifies the active artifact.

### Source-audio map

Each archived clip is represented by a record with this shape:

```json
{
  "clip_id": "human-0-styledubber",
  "case_id": "human-0",
  "artifact_path": "styledubber.mp4",
  "visual_source": "browser-capture/examples-human-0-styledubber.webm",
  "audio_source": "apps/web/public/showcases/v2/human-0/styledubber.mp4#a:0",
  "in_frame_label": "AUDIBLE: StyleDubber",
  "content_status": "archived_research_example"
}
```

The build must reject a film specification where `audio_source` and `artifact_path` resolve to different artifacts.

## Failure handling

- If a V1 narration range cannot be extracted or has no audio stream, the V3 build fails before producing an MP4.
- If an archived artifact has no audio stream, its browser-capture command and source-audio-map validation fail; the clip is not silently replaced by GT audio or silence.
- If a gallery ref is missing, the controller still sets state but does not throw; registered players remain safe to pause and reset.
- If a video refuses autoplay, native user controls remain available and playback behavior is still correct after a user gesture.
- If source-evidence status changes to `blocked`, both gallery and V3 film builders must exclude that case rather than present a stale asset.

## Test and release gates

### Frontend tests

1. Playing HPMDubbing pauses and resets GT, StyleDubber, and EmoDubber.
2. Playing each artifact gives it the only active `AUDIBLE:` label and active-panel class.
3. Switching case pauses and resets players from the previous case.
4. The female task panel contains `TASK ILLUSTRATION` and does not contain `human-0 / GT audio`.
5. The timeline contains English IPA and illustrated PROSODY/OUTPUT source labels.
6. Reduced-motion and keyboard control behavior remain intact.

### Video checks

1. `ffprobe` confirms H.264, AAC, `mov_text`, 1920x1080, 30 FPS, and an expected duration in the 100–112 s window.
2. The audio map contains eight case/artifact entries, all unique, all matching the visible active artifact.
3. Narration source ranges reference the V1 video and do not overlap an archived artifact-audio segment.
4. EBU R128 reports the narration delivery target and sample playback is audibly present.
5. Contact-sheet and transition-frame inspection finds no blank/white frames, crop errors, or stale `AUDIBLE: GT` labels on method clips.
6. SHA-256, delivery manifest, SRT, fact-check, source-audio map, clean-clone build, and static documentation links pass together.

## Explicit exclusions

- No new model checkpoint, training, benchmark, score, or claim of real-time generation.
- No addition of human-recorded narration.
- No replacement of historical method audio with GT audio, synthetic speech, or a generic soundtrack.
- No modification to V1 or V2 release assets, manifests, tags, or audit reports.
