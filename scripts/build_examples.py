#!/usr/bin/env python3
"""Build small, redistributable OpenDub alpha projects from synthetic media."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from opendub.domain.assets import ConsentRecord, VoiceReference
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Create redistributable OpenDub alpha examples.")
    parser.add_argument("--workspace", type=Path, required=True, help="Destination OpenDub workspace.")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    projects = (
        ("Authorized demo", "An authorized voice reference enters a local dubbing timeline."),
        ("Lecture timing demo", "A second synthetic cue demonstrates target timing."),
    )
    for name, cue in projects:
        project = build_project(workspace, name, cue)
        print(f"Created {project.name} ({project.id})")


def build_project(workspace: Path, name: str, cue_text: str):
    """Create a minimal project using FFmpeg-generated visual and audio media."""
    store = ProjectStore(workspace)
    project = store.create(name)
    source_dir = workspace / "example-source" / project.id
    source_dir.mkdir(parents=True, exist_ok=True)
    video_path = source_dir / "synthetic-video.mp4"
    reference_path = source_dir / "self-recorded-reference.wav"
    subtitle_path = source_dir / "dialogue.srt"
    _run_ffmpeg(
        [
            "-f",
            "lavfi",
            "-i",
            "testsrc2=size=640x360:rate=30:duration=2",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ]
    )
    _run_ffmpeg(
        [
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=220:sample_rate=24000:duration=2",
            "-ac",
            "1",
            str(reference_path),
        ]
    )
    subtitle_path.write_text(f"1\n00:00:00,200 --> 00:00:01,700\n{cue_text}\n", encoding="utf-8")

    artifacts = ArtifactStore(workspace)
    video = artifacts.ingest_bytes(
        project.id,
        kind="video",
        display_name="synthetic-video.mp4",
        data=video_path.read_bytes(),
        extension="mp4",
    )
    project = project.add_asset(video, expected_revision=project.revision)
    store.save(project, expected_revision=1)
    reference_audio = artifacts.ingest_bytes(
        project.id,
        kind="audio",
        display_name="self-recorded-reference.wav",
        data=reference_path.read_bytes(),
        extension="wav",
    )
    project = project.add_asset(reference_audio, expected_revision=project.revision)
    store.save(project, expected_revision=2)
    subtitles = artifacts.ingest_bytes(
        project.id,
        kind="subtitle",
        display_name="dialogue.srt",
        data=subtitle_path.read_bytes(),
        extension="srt",
    )
    project = project.add_asset(subtitles, expected_revision=project.revision)
    store.save(project, expected_revision=3)
    consent = ConsentRecord(material_source="self_recorded")
    voice_reference = VoiceReference(
        asset_id=reference_audio.id,
        consent_id=consent.id,
        speaker_label="Synthetic narrator",
    )
    project = project.add_voice_reference(
        consent, voice_reference, expected_revision=project.revision
    )
    store.save(project, expected_revision=4)
    segment = DubbingSegment(
        id=new_id(),
        range=TimeRange(start_us=200_000, end_us=1_700_000),
        text=cue_text,
        language="en",
        character_id=new_id(),
        voice_reference_id=voice_reference.id,
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="galaxycong/emodubber",
        status="ready",
    )
    project = project.add_segment(segment, expected_revision=project.revision)
    store.save(project, expected_revision=5)
    return project


def _run_ffmpeg(arguments: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", *arguments], check=True, capture_output=True, text=True)


if __name__ == "__main__":
    main()
