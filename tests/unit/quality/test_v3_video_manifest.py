from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[3]
VIDEO_DIR = ROOT / "docs/grant/video/v3"


def _probe(video: Path) -> dict[str, object]:
    output = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
            "-of",
            "json",
            str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(output.stdout)


def test_v3_delivery_manifest_describes_a_complete_narrated_evidence_film() -> None:
    manifest_path = VIDEO_DIR / "delivery-manifest.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "opendub.video-delivery/v3"
    assert manifest["release"] == "v3.0.0-narrated-evidence"
    video = VIDEO_DIR / manifest["video"]["path"]
    assert video.is_file()
    assert 111.5 <= manifest["video"]["duration_seconds"] <= 112.1
    assert {item["path"] for item in manifest["supporting_files"]} >= {
        "OpenDub_Narrated_Evidence_Walkthrough_v3.0.0.mp4",
        "OpenDub_Narrated_Evidence_Walkthrough_v3.0.0_CN_EN.srt",
        "source-audio-map.json",
        "fact-check.md",
        "narration-map.zh-CN.md",
    }

    probe = _probe(video)
    streams = probe["streams"]
    assert isinstance(streams, list)
    assert any(
        stream["codec_type"] == "video" and stream["codec_name"] == "h264" for stream in streams
    )
    assert any(
        stream["codec_type"] == "audio" and stream["codec_name"] == "aac" for stream in streams
    )
    assert any(
        stream["codec_type"] == "subtitle" and stream["codec_name"] == "mov_text"
        for stream in streams
    )
    video_stream = next(stream for stream in streams if stream["codec_type"] == "video")
    assert (video_stream["width"], video_stream["height"], video_stream["r_frame_rate"]) == (
        1920,
        1080,
        "30/1",
    )
