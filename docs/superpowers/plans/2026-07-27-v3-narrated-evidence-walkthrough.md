# V3 Narrated Evidence Walkthrough Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Deliver OpenDub V3 with a female-scene task illustration, exclusive artifact-specific example playback, and a new application film that reuses V1 Chinese synthetic narration while preserving each archived method artifact's own audio.

**Architecture:** Keep V2's top-level VTTS flow and replace its lower cue region with an audio-free React task illustration. A gallery-local playback controller owns a single active artifact. A JSON source-audio map proves every archival clip's visible artifact and audio asset match.

**Tech Stack:** React 18, TypeScript, Vitest, Testing Library, CSS, Python 3.13, FFmpeg/FFprobe, Playwright, Bash, JSON, SHA-256.

## Global Constraints

- Female scene: TASK ILLUSTRATION, not a case, audio source, transcript, Replay, or Live claim.
- Timeline: English IPA plus illustrated pitch/energy and waveform only.
- Archived gallery: one moving and audible video; inactive videos are paused, reset to zero, and muted.
- Narration: V1 MP4 audio stream only, absent during archive clips.
- Delivery: new docs/grant/video/v3 path and v3.0.0-narrated-evidence identity; V1/V2 files and tags remain immutable.
- Status: human-0 and animation-1 always remain Archived research example.
- Release: full checks, clean clone, and independent audit >= 9 / 10 with no P0/P1 blocker.

---

### Task 1: Build the isolated task-illustration component

**Files:**
- Create: apps/web/src/features/vtts/TaskIllustrationPanel.tsx
- Create: apps/web/src/features/vtts/task-illustration-panel.css
- Create: apps/web/src/features/vtts/TaskIllustrationPanel.test.tsx
- Modify: apps/web/src/features/vtts/VttsTaskStagePage.tsx
- Modify: apps/web/src/features/vtts/vtts-task-stage.css

**Interfaces:**
- Produces: TaskIllustrationPanel(): JSX.Element.
- Produces: TASK_ILLUSTRATION_IPA, a readonly English IPA token array.
- Consumes: apps/web/public/atlas/demo/scene-v1.png only. It owns no audio or video element.

- [ ] **Step 1: Write failing component tests**

Create TaskIllustrationPanel.test.tsx:

    it("labels the female scene as task illustration, not a historical case", () => {
      render(<TaskIllustrationPanel />);
      expect(screen.getByText(/task illustration/i)).toBeVisible();
      expect(screen.getByText(/no case audio or transcript/i)).toBeVisible();
      expect(screen.queryByText(/human-0\s*\/\s*gt audio/i)).not.toBeInTheDocument();
    });

    it("keeps English IPA and illustrated signal tracks on one playhead", async () => {
      const user = userEvent.setup();
      render(<TaskIllustrationPanel />);
      expect(screen.getByText("ðə")).toBeVisible();
      expect(screen.getByText("ˈtʃeɪn.dʒɪz")).toBeVisible();
      expect(screen.getByText(/illustrated pitch \+ energy/i)).toBeVisible();
      expect(screen.getByText(/illustrated target speech/i)).toBeVisible();
      await user.click(screen.getByRole("button", { name: /hide face overlay/i }));
      expect(screen.queryByText(/face affect/i)).not.toBeInTheDocument();
    });

- [ ] **Step 2: Confirm the test fails**

    npm --prefix apps/web run test -- --run src/features/vtts/TaskIllustrationPanel.test.tsx

Expected: FAIL because TaskIllustrationPanel does not exist.

- [ ] **Step 3: Implement the component**

Implement this state contract:

    export const TASK_ILLUSTRATION_IPA = [
      "ðə", "siːn", "ˈtʃeɪn.dʒɪz", "haʊ", "ə", "laɪn", "ʃʊd", "saʊnd",
    ] as const;

    export function TaskIllustrationPanel() {
      const [faceVisible, setFaceVisible] = useState(true);
      const [lipVisible, setLipVisible] = useState(true);
      const [progress, setProgress] = useState(42);
      const [playing, setPlaying] = useState(false);
    }

Use an interval only while playing and clear it in effect cleanup. Render exact labels TASK ILLUSTRATION · CONCEPT SCENE and TASK ILLUSTRATION · NO CASE AUDIO OR TRANSCRIPT. Keep One scene carries several timing cues. Render female filmstrip, Face/Lip toggles, English IPA, illustrated two-curve PROSODY, illustrated waveform OUTPUT, range input, and shared playhead.

- [ ] **Step 4: Replace only the V2 cue/timeline markup**

In VttsTaskStagePage.tsx, remove the human-0 feature fetch, task-video ref, cue microscope, and real-feature timeline. Keep the V2 top task flow and its Task illustration · no fresh run labels. Render TaskIllustrationPanel after the flow and ExampleGalleryPage after it. Move female styles to the new CSS file and remove only unreachable selectors from vtts-task-stage.css.

- [ ] **Step 5: Verify and commit**

    npm --prefix apps/web run test -- --run src/features/vtts/TaskIllustrationPanel.test.tsx src/features/vtts/VttsTaskStagePage.test.tsx
    npm --prefix apps/web run check
    npm --prefix apps/web run build
    git add apps/web/src/features/vtts
    git commit -m "feat(vtts): restore illustrated synchronized task panel"

Expected: selected tests, type check, and production build pass.

### Task 2: Make archived playback exclusive and artifact-specific

**Files:**
- Create: apps/web/src/features/showcases/useExclusiveShowcasePlayback.ts
- Create: apps/web/src/features/showcases/useExclusiveShowcasePlayback.test.tsx
- Modify: apps/web/src/features/showcases/ExampleGalleryPage.tsx
- Modify: apps/web/src/features/showcases/ExampleGalleryPage.test.tsx
- Modify: apps/web/src/features/showcases/example-gallery.css

**Interfaces:**
- Produces: useExclusiveShowcasePlayback() with activeArtifactPath, registerPlayer, handlePlay, handlePause, resetAll.
- Consumes: case ID, artifact path, and each panel HTMLVideoElement.
- Guarantees: active player is unmuted; every inactive player is paused, zeroed, and muted.

- [ ] **Step 1: Write failing playback tests**

Create a hook test with fake videos:

    result.current.registerPlayer("gt.mp4", gt);
    result.current.registerPlayer("hpmdubbing.mp4", hpm);
    result.current.registerPlayer("styledubber.mp4", style);
    result.current.handlePlay("human-0", "styledubber.mp4", style);

    expect(result.current.activeArtifactPath).toBe("styledubber.mp4");
    expect(gt.pause).toHaveBeenCalled();
    expect(hpm.pause).toHaveBeenCalled();
    expect(gt.currentTime).toBe(0);
    expect(hpm.currentTime).toBe(0);
    expect(style.muted).toBe(false);

Extend ExampleGalleryPage.test.tsx: playing StyleDubber renders AUDIBLE: StyleDubber, applies is-active-artifact, and does not render AUDIBLE: Ground truth. Switching case pauses/resets prior players.

- [ ] **Step 2: Confirm the tests fail**

    npm --prefix apps/web run test -- --run src/features/showcases/useExclusiveShowcasePlayback.test.tsx src/features/showcases/ExampleGalleryPage.test.tsx

Expected: FAIL because controller and source-specific label do not exist.

- [ ] **Step 3: Implement the controller and UI binding**

Use useRef(new Map<string, HTMLVideoElement>()) and useState<string | null>(null). For every inactive player run:

    player.pause();
    player.currentTime = 0;
    player.muted = true;

For selected player run player.muted = false before saving its path. resetAll resets every player and clears active state; run it on case change and unmount. Registering null removes map entry.

Keep native video controls and use the sole source:

    src={publicShowcaseUrl(caseItem.id, artifact.path)}

Add active-panel status using string concatenation:

    <article className={isActive ? "example-media-panel is-active-artifact" : "example-media-panel"}>
      <span className="example-video-status">
        {isPlaying ? "AUDIBLE: " + artifact.label : "READY · audio idle"}
      </span>
    </article>

Inactive styling may dim a panel but never cover controls or block keyboard use.

- [ ] **Step 4: Verify and commit**

    npm --prefix apps/web run test -- --run src/features/showcases
    npm --prefix apps/web run check
    npm --prefix apps/web run build
    git add apps/web/src/features/showcases
    git commit -m "feat(showcases): make artifact playback exclusive and audible"

Expected: all showcase tests pass and controls remain accessible.

### Task 3: Create the V3 source-audio map and validator

**Files:**
- Create: docs/grant/video/v3/source-audio-map.json
- Create: scripts/verify_v3_audio_map.py
- Create: tests/unit/quality/test_v3_audio_map.py
- Create: docs/grant/video/v3/fact-check.md
- Create: docs/grant/video/v3/narration-map.zh-CN.md

**Interfaces:**
- Produces: verify_audio_map(path: Path, root: Path, require_captures: bool) -> list[str].
- Produces: six V1 narration records and eight unique case/artifact records.
- Rejects: archive audio that differs from the visible artifact.

- [ ] **Step 1: Write failing Python tests**

    def test_rejects_audio_different_from_visible_artifact(tmp_path: Path) -> None:
        payload = valid_payload()
        payload["archive_clips"][0]["audio_source"] = (
            "apps/web/public/showcases/v2/human-0/gt.mp4#a:0"
        )
        payload["archive_clips"][0]["artifact_path"] = "styledubber.mp4"
        assert any(
            "must use the visible artifact" in issue
            for issue in verify_audio_map(write(payload), tmp_path, False)
        )

    def test_requires_eight_unique_case_artifact_pairs(tmp_path: Path) -> None:
        payload = valid_payload()
        payload["archive_clips"] = payload["archive_clips"][:-1]
        assert any(
            "exactly eight" in issue
            for issue in verify_audio_map(write(payload), tmp_path, False)
        )

- [ ] **Step 2: Confirm the tests fail**

    .venv/bin/pytest tests/unit/quality/test_v3_audio_map.py -v

Expected: FAIL because source-map validation does not exist.

- [ ] **Step 3: Implement mapping and validation**

Set schema_version to opendub.v3-source-audio-map/v1. Add narration ranges 00:00–00:14, 00:14–00:28, 00:28–00:50, 00:50–01:07, 01:23–01:38, and 01:38–01:50 from the V1 MP4.

Add exactly eight archive items covering GT, HPMDubbing, StyleDubber, and EmoDubber for both cases. Each matching source has this form:

    {
      "case_id": "human-0",
      "artifact_path": "styledubber.mp4",
      "audio_source": "apps/web/public/showcases/v2/human-0/styledubber.mp4#a:0",
      "in_frame_label": "AUDIBLE: StyleDubber",
      "content_status": "archived_research_example"
    }

Validate schema, six narration ranges, eight unique pairs, all expected pairs, matching audio/artifact path, matching label, existing public MP4s, and capture existence when require_captures is true. Print issues to stderr and exit 2 on failure.

- [ ] **Step 4: Verify and commit**

    .venv/bin/pytest tests/unit/quality/test_v3_audio_map.py -v
    .venv/bin/python scripts/verify_v3_audio_map.py docs/grant/video/v3/source-audio-map.json
    git add docs/grant/video/v3/source-audio-map.json docs/grant/video/v3/fact-check.md \
      docs/grant/video/v3/narration-map.zh-CN.md scripts/verify_v3_audio_map.py \
      tests/unit/quality/test_v3_audio_map.py
    git commit -m "feat(video): define V3 narration and artifact audio map"

Expected: tests and real-map validation pass before captures are required.
+
### Task 4: Capture V3 browser evidence

**Files:**
- Create: scripts/capture_v3_web_clips.mjs
- Create: docs/grant/video/v3/README.md
- Create: docs/grant/video/v3/assets/browser-captures/.gitkeep
- Modify: package.json
- Modify: pnpm-lock.yaml
- Modify: tests/unit/quality/test_v3_audio_map.py

**Interfaces:**
- Consumes: Vite at http://127.0.0.1:5181, V3 UI labels, and source-audio-map visual_source paths.
- Produces: two task clips and eight archive visual clips at exactly those paths.

- [ ] **Step 1: Add a failing capture-inventory test**

Add test_require_captures_rejects_missing_visual: use a valid map with one missing visual_source, call verify_audio_map with require_captures true, and expect browser capture is missing.

- [ ] **Step 2: Implement deterministic Playwright capture**

capture_v3_web_clips.mjs opens Chromium at 1920x1080, captures /vtts?tour=flow, captures the task illustration after Face/Lip interaction, then captures each map item by opening /examples, selecting its case, clicking the target native video, waiting for its AUDIBLE label, and recording at least three seconds. The film builder trims every archive segment to 2.25 seconds, which keeps the complete delivery inside the 112-second limit.

The script records browser visual only. FFmpeg adds audio later. It fails when a map visual path, accessible video label, or AUDIBLE status is missing. It writes exactly the map visual_source paths.

- [ ] **Step 3: Capture, verify, document, and commit**

    npm --prefix apps/web run dev -- --port 5181
    node scripts/capture_v3_web_clips.mjs
    .venv/bin/python scripts/verify_v3_audio_map.py --require-captures docs/grant/video/v3/source-audio-map.json
    git add scripts/capture_v3_web_clips.mjs docs/grant/video/v3 package.json pnpm-lock.yaml \
      tests/unit/quality/test_v3_audio_map.py
    git commit -m "feat(video): capture V3 task and artifact interactions"

Document prerequisites, viewport, and that capture audio is discarded in favor of validated audio mapping.

### Task 5: Build the narrated V3 film and metadata

**Files:**
- Create: scripts/build_v3_showcase_film.sh
- Create: scripts/update_v3_video_manifest.py
- Create: docs/grant/video/v3/OpenDub_VTTS_Narrated_Evidence_v3.0.0_CN_EN.srt
- Create: docs/grant/video/v3/delivery-manifest.json
- Create: docs/grant/video/v3/OpenDub_VTTS_Narrated_Evidence_v3.0.0.sha256
- Create: tests/unit/quality/test_v3_video_manifest.py

**Interfaces:**
- Consumes: V1 narration MP4, V3 map, V3 browser captures, public method MP4s, SRT, FFmpeg.
- Produces: V3 MP4, contact sheet, SHA file, and delivery manifest.
- Produces: update_manifest(video_dir: Path) -> dict[str, object].

- [ ] **Step 1: Write failing manifest tests**

    def test_manifest_requires_source_audio_map_hash(tmp_path: Path) -> None:
        manifest = update_manifest(build_tiny_h264_aac_subtitle_fixture(tmp_path))
        assert manifest["source_audio_map"]["sha256"]

    def test_manifest_reports_required_streams(tmp_path: Path) -> None:
        manifest = update_manifest(build_tiny_h264_aac_subtitle_fixture(tmp_path))
        assert manifest["video"]["audio"].startswith("AAC")
        assert manifest["video"]["subtitle"].startswith("mov_text")

- [ ] **Step 2: Confirm the tests fail**

    .venv/bin/pytest tests/unit/quality/test_v3_video_manifest.py -v

Expected: FAIL because V3 film tooling does not exist.

- [ ] **Step 3: Implement audio-safe FFmpeg assembly**

The builder first runs the V3 map validator. It defines these constructors:

    make_narrated_clip "01-identity" "$capture" "00:00:00" "14"
    make_archive_clip "human-0-styledubber" "$capture" \
      "apps/web/public/showcases/v2/human-0/styledubber.mp4" \
      "AUDIBLE: StyleDubber" "2.25"

make_narrated_clip extracts V1 a:0, applies loudnorm=I=-16:TP=-1:LRA=11, and pairs it with a task/method/evidence browser visual. make_archive_clip maps browser 0:v and exact public artifact 1:a:0, then draws AUDIBLE label plus ARCHIVED RESEARCH EXAMPLE · Not a fresh OpenDub run.

No archive clip maps audio from fixed GT. Concatenate: identity, task illustration, four human clips, four animation clips, methods, canvas, evidence, close. Encode 1920x1080/30 FPS H.264/AAC, add bilingual SRT as mov_text, create contact sheet, update manifest, then write relative-path SHA-256.

- [ ] **Step 4: Implement subtitles and manifest contract**

The SRT labels the female panel as a task illustration and each archive segment as historical. The updater requires H.264, AAC, mov_text, 1920x1080, 30 FPS, duration 100–112 seconds, matching SRT/map hashes, and release v3.0.0-narrated-evidence. It refuses V1/V2 delivery paths.

- [ ] **Step 5: Build, inspect, verify, and commit**

    bash scripts/build_v3_showcase_film.sh
    .venv/bin/pytest tests/unit/quality/test_v3_video_manifest.py -v
    .venv/bin/python scripts/verify_v3_audio_map.py --require-captures docs/grant/video/v3/source-audio-map.json
    cd docs/grant/video/v3 && sha256sum -c OpenDub_VTTS_Narrated_Evidence_v3.0.0.sha256
    ffprobe -v error -show_entries format=duration:stream=codec_name,codec_type,width,height,r_frame_rate \
      OpenDub_VTTS_Narrated_Evidence_v3.0.0.mp4
    git add scripts/build_v3_showcase_film.sh scripts/update_v3_video_manifest.py \
      docs/grant/video/v3 tests/unit/quality/test_v3_video_manifest.py
    git commit -m "feat(video): publish narrated V3 evidence walkthrough"

Inspect contact-sheet and every clip boundary: narration is audible in narration clips; archive clips contain only named artifact audio; no method clip displays AUDIBLE: GT.

### Task 6: Complete quality, audit, and release

**Files:**
- Modify: README.md
- Modify: CHANGELOG.md
- Modify: docs/PROJECT_CURRENT_STATE.md
- Create: TODO/08_V3_NARRATED_EVIDENCE/README.md
- Create: TODO/08_V3_NARRATED_EVIDENCE/01_RELEASE_CHECKLIST.md
- Create: review/round-05-v3-strict-audit.md

**Interfaces:**
- Produces: public V3 status that distinguishes task illustration, archived samples, platform narration, V1/V2 history, and audit result.

- [ ] **Step 1: Add factual V3 release documentation**

The V3 checklist includes:

    [ ] Task illustration has no case-audio claim.
    [ ] Eight archive clips have matching visual and audio artifacts.
    [ ] Narration is extracted from V1 and absent from archive clips.
    [ ] V3 MP4/SRT/source-map hashes validate.
    [ ] make check and documentation links pass.
    [ ] A clean clone rebuilds the Web app and verifies V3 media.
    [ ] Independent strict audit is at least 9/10.
    [ ] Formal V3 tag has been pushed and remote clean clone validation passed.

Until final audit and tag, docs call V3 a candidate and retain V2 as the released predecessor.

- [ ] **Step 2: Run full local gates and browser QA**

    make check
    .venv/bin/python scripts/check_docs_links.py
    .venv/bin/python scripts/verify_registry.py model-registry/upstreams.yaml
    .venv/bin/opendub atlas validate --content content
    .venv/bin/python scripts/verify_v3_audio_map.py --require-captures docs/grant/video/v3/source-audio-map.json
    cd docs/grant/video/v3 && sha256sum -c OpenDub_VTTS_Narrated_Evidence_v3.0.0.sha256

At 1920x1080, 1440x900, 1280x720, 768x1024, and 390x844, verify Face/Lip toggles, timeline controls, eight individual plays, active highlighter, case-tab reset, native controls, and reduced motion. Save screenshots under .opendub/v3-qa/, never under reference/.

- [ ] **Step 3: Obtain and close strict audit**

Request independent review of narration audibility, eight visual/audio pairings, task-illustration boundary, no stale GT mapping, interaction behavior, source-map validation, hashes, and grant suitability. Save it as review/round-05-v3-strict-audit.md.

For any score below 9 / 10, repair every P0/P1 release blocker, rerun targeted and full media checks, rebuild hashes, and obtain the next numbered audit. Continue until an audit reports >= 9 / 10 with no P0/P1 blocker.

- [ ] **Step 4: Tag, push, and prove remote delivery**

    git add README.md CHANGELOG.md docs/PROJECT_CURRENT_STATE.md TODO/08_V3_NARRATED_EVIDENCE review
    git commit -m "docs(release): close V3 narrated evidence audit"
    git tag -a v3.0.0-narrated-evidence -m "OpenDub V3 narrated evidence release"
    git push origin main
    git push origin v3.0.0-narrated-evidence
    release_dir=$(mktemp -d /tmp/opendub-v3-release.XXXXXX)
    git clone --depth 1 --branch v3.0.0-narrated-evidence git@github.com:wsincos/OpenDub.git "$release_dir"
    cd "$release_dir"
    npm exec --yes --package=pnpm@9.15.0 -- pnpm install --frozen-lockfile
    npm exec --yes --package=pnpm@9.15.0 -- pnpm --filter @opendub/web build
    cd docs/grant/video/v3
    sha256sum -c OpenDub_VTTS_Narrated_Evidence_v3.0.0.sha256

Expected: remote tag resolves to release commit; clean-clone Web build and V3 SHA validation pass. If post-release verification needs recording, add a separate documentation commit without moving V3 tag.

## Plan self-review

Coverage: Task 1 restores task illustration; Task 2 fixes artifact playback; Tasks 3–5 make narration and all eight audio pairings deterministic and verifiable; Task 6 completes QA, audit, tag, and remote verification.

Consistency: the sole archive identity is case ID plus artifact path across React state, capture, map validation, FFmpeg audio selection, on-screen label, and release checks. V1 narration and archive audio never share a clip.

Scope: no model runtime, human narration, benchmark, or V1/V2 delivery modification.
