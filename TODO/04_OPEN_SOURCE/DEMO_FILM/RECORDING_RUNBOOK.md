# Recording Runbook

## 48 Hours Before Capture

1. Create `release/demo-film` from the intended tag and record its commit.
2. Run `make check`, Atlas validation and Playwright; archive the results.
3. Generate `content/content-lock.json` and record its SHA-256 in the shot log.
4. Copy the approved case to an isolated demo directory; do not operate on research originals.
5. Verify video, voice, text, music, fonts and screenshots against `ASSET_AND_RIGHTS.md`.
6. Cache all Replay media locally. Disable notifications, desktop sync banners, personal bookmarks and browser autofill.
7. Decide branch A or B of shots 17-18 by running the comparison gate.

## Environment

| Item | Setting |
|---|---|
| Capture | 3840x2160, 60 FPS, Rec.709 |
| Edit | 1920x1080, 30 FPS, 48kHz/24bit |
| Browser | dedicated profile, 100% zoom, no extensions |
| App | production build, not development overlays |
| Cursor | visible small dot, no exaggerated trail |
| Motion | default and reduced-motion plates both captured |
| Audio | record system/app audio on separate tracks if available |

## Atlas Capture Passes

### Pass 1: Full narrative

Perform the full 2:40 path without speaking. Capture from `/explore` to `/evidence`. This supplies the natural cursor rhythm and backup coverage.

### Pass 2: Clean interaction plates

Record each shot in the table independently. Reset route and timeline cursor before every take. The operator may remove wait time in edit but cannot fabricate state changes.

### Pass 3: State proof

Capture Evidence Room rows, content mode labels, comparison gate result, content-lock, and, only when applicable, Live run metadata. These are short inserts used to support voiceover claims.

### Pass 4: Failure plates

Capture checkpoint unavailable, missing signal and comparison gate failed states. These plates are not mandatory in the master cut but prove that the product degrades honestly.

## Voiceover

- Record at 48kHz/24bit with 10 seconds of room tone.
- Speak in calm, precise Mandarin at 175 to 195 characters per minute.
- Record each script section separately and leave 1.5 seconds of room after sections 0, 17A/17B and 22.
- Do not add claims while recording; use the approved script exactly.

## Editing Handoff

```text
demo-film/
  source-video/
  screen-capture/
  voiceover/
  compare-audio/
  graphics/
  project-files/
  exports/
  evidence/
```

The `evidence/shot-log.csv` row contains: shot ID, take, route, method/case, mode, commit, content-lock, source asset IDs, reviewer and approval status.
