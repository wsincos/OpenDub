from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def _load_validator() -> ModuleType:
    path = Path(__file__).parents[3] / "scripts" / "verify_v3_audio_map.py"
    spec = importlib.util.spec_from_file_location("verify_v3_audio_map", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _label_for(artifact_path: str) -> str:
    return {
        "gt.mp4": "Ground truth",
        "hpmdubbing.mp4": "HPMDubbing",
        "styledubber.mp4": "StyleDubber",
        "emodubber.mp4": "EmoDubber",
    }[artifact_path]


def valid_payload() -> dict[str, object]:
    narration_source = "docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4#a:0"
    archive_clips = []
    for case_id in ("human-0", "animation-1"):
        for artifact_path in ("gt.mp4", "hpmdubbing.mp4", "styledubber.mp4", "emodubber.mp4"):
            stem = artifact_path.removesuffix(".mp4")
            archive_clips.append(
                {
                    "clip_id": f"{case_id}-{stem}",
                    "case_id": case_id,
                    "artifact_path": artifact_path,
                    "visual_source": (
                        f"docs/grant/video/v3/assets/browser-captures/{case_id}-{stem}.webm"
                    ),
                    "audio_source": f"apps/web/public/showcases/v2/{case_id}/{artifact_path}#a:0",
                    "in_frame_label": f"AUDIBLE: {_label_for(artifact_path)}",
                    "content_status": "archived_research_example",
                }
            )

    return {
        "schema_version": "opendub.v3-source-audio-map/v1",
        "narration_source": narration_source,
        "narration_clips": [
            {"clip_id": "identity", "source_range": "00:00-00:14", "subtitle_id": 1},
            {"clip_id": "task", "source_range": "00:14-00:28", "subtitle_id": 2},
            {"clip_id": "methods", "source_range": "00:28-00:50", "subtitle_id": "3-4"},
            {"clip_id": "canvas", "source_range": "00:50-01:07", "subtitle_id": 5},
            {"clip_id": "evidence", "source_range": "01:23-01:38", "subtitle_id": 7},
            {"clip_id": "close", "source_range": "01:38-01:50", "subtitle_id": "8-9"},
        ],
        "archive_clips": archive_clips,
    }


def _write_payload(root: Path, payload: dict[str, object]) -> Path:
    (root / "docs/grant/video").mkdir(parents=True, exist_ok=True)
    narration_path = root / "docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4"
    narration_path.write_bytes(b"v1")
    for clip in payload["archive_clips"]:  # type: ignore[index]
        assert isinstance(clip, dict)
        audio_path = str(clip["audio_source"]).split("#", maxsplit=1)[0]
        path = root / audio_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"artifact")
    path = root / "source-audio-map.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_rejects_audio_different_from_visible_artifact(tmp_path: Path) -> None:
    validator = _load_validator()
    payload = valid_payload()
    archive_clips = payload["archive_clips"]
    assert isinstance(archive_clips, list)
    first = archive_clips[0]
    assert isinstance(first, dict)
    first["artifact_path"] = "styledubber.mp4"
    first["audio_source"] = "apps/web/public/showcases/v2/human-0/gt.mp4#a:0"

    issues = validator.verify_audio_map(_write_payload(tmp_path, payload), tmp_path, False)

    assert any("must use the visible artifact" in issue for issue in issues)


def test_requires_eight_unique_case_artifact_pairs(tmp_path: Path) -> None:
    validator = _load_validator()
    payload = valid_payload()
    archive_clips = payload["archive_clips"]
    assert isinstance(archive_clips, list)
    archive_clips.pop()

    issues = validator.verify_audio_map(_write_payload(tmp_path, payload), tmp_path, False)

    assert any("exactly eight" in issue for issue in issues)


def test_accepts_complete_map_and_requires_captures_only_when_requested(tmp_path: Path) -> None:
    validator = _load_validator()
    payload = valid_payload()
    path = _write_payload(tmp_path, payload)

    assert validator.verify_audio_map(path, tmp_path, False) == []
    issues = validator.verify_audio_map(path, tmp_path, True)
    assert any("missing visual capture" in issue for issue in issues)
