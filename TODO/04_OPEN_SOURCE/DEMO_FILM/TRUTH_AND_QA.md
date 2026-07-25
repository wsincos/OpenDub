# Truth, Review and Delivery QA

## Claim Matrix

| Claim or image | Evidence required | Never substitute |
|---|---|---|
| Video-aware task | paper-consistent Task Explorer and input cues | a generic video player |
| HPM/Style/Emo method detail | approved manifest nodes and paper anchors | recreated paper figure with no source |
| Concept signal | `concept + illustrative` label | a chart presented as live activation |
| Replay audio/video | bundle hash, rights, source mode | a downloaded file with no provenance |
| Live model | successful local run, source commit, weights hash, run manifest | Replay playback or edited progress bar |
| A/B/C comparison | comparison gate passing common input hashes | different upstream demos |
| emotion intensity control | matching Replay variants or a measured Live control test | volume changes |
| open source | public repository, license, docs and released content | a local-only screen recording |

## Pre-recording Checklist

- [ ] `git rev-parse HEAD` is written in the shot log.
- [ ] `content-lock.json` hash is written in the shot log.
- [ ] Every route in SHOTLIST loads in production build.
- [ ] All video/audio assets are locally cached and rights-approved.
- [ ] Every visible state badge agrees with the content manifest.
- [ ] The comparison branch is chosen from a recorded gate result.
- [ ] No demo screen exposes local paths, tokens, email, unlicensed media or private model URLs.
- [ ] The exact master script is fact-checked by a method reviewer.

## Technical Review

The reviewer signs off on:

- input/output definition;
- HPM Lip/Face/Scene mapping;
- Style MPA/PLA/USL mapping;
- Emo LPA/PE/Speaker/FUEC/PNGM mapping;
- status labels;
- metric labels and applicability;
- paper/source/commit links;
- output audio source and loudness treatment.

## Visual and Audio Review

- [ ] 1080p, laptop and mobile preview text remains readable.
- [ ] No node, signal or subtitle overlaps the lips or key labels.
- [ ] There is no blank video, blank graph canvas or missing waveform.
- [ ] A/B/C has no overlapping audio.
- [ ] Comparison candidates use the same listening gain policy.
- [ ] Music is absent during candidate listening.
- [ ] Concept/Replay/Live labels are legible for at least 1.5 seconds when first introduced.
- [ ] End card remains for at least 4 seconds.

## Delivery

```text
OpenDub_DemoFilm_Delivery/
  master/OpenDub_MethodAtlas_2m40_Master.mov
  web/OpenDub_MethodAtlas_2m40_CN_EN.mp4
  web/OpenDub_MethodAtlas_60s.mp4
  web/OpenDub_MethodAtlas_30s_Loop.mp4
  captions/OpenDub_MethodAtlas_CN.srt
  captions/OpenDub_MethodAtlas_EN.srt
  stills/OpenDub_MethodAtlas_EndCard.png
  evidence/shot-log.csv
  evidence/fact-check.md
  evidence/content-lock.txt
  evidence/asset-rights-register.xlsx
  checksums.txt
```

The final fact-check must be repeated after the last edit. Any shot that changes state meaning, method identity or media source requires a new review.
