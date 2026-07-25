"""Render accepted candidate takes into a local dubbing track and optional MP4."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import soundfile as sf  # type: ignore[import-untyped]

from opendub.domain.assets import MediaAsset
from opendub.domain.errors import DomainError
from opendub.media.render import (
    AI_DUBBING_LABEL,
    MixMode,
    TimelineAudioClip,
    assemble_dubbing_track,
    mux_video,
)
from opendub.storage.project_store import ProjectStore


@dataclass(frozen=True)
class RenderResult:
    """Portable locations for one local render operation."""

    dubbing_audio: Path
    video: Path | None
    manifest: Path
    sample_rate: int
    mode: MixMode
    distribution_authorized: bool


class RenderService:
    """Build exports only from candidates explicitly accepted in the project manifest."""

    def __init__(self, store: ProjectStore) -> None:
        self.store = store

    def render(self, project_id: str, *, mode: MixMode) -> RenderResult:
        """Assemble current accepted candidates and mux a project video when one exists."""
        project = self.store.load(project_id)
        candidates = {candidate.id: candidate for candidate in project.candidates}
        assets = {asset.id: asset for asset in project.assets}
        clips: list[TimelineAudioClip] = []
        for segment in project.segments:
            if segment.accepted_candidate_id is None:
                continue
            candidate = candidates.get(segment.accepted_candidate_id)
            if candidate is None:
                raise DomainError(
                    code="INPUT_INVALID",
                    message="Accepted candidate record is missing from the project.",
                )
            audio_asset = assets.get(candidate.audio_asset_id)
            if audio_asset is None or audio_asset.kind != "audio":
                raise DomainError(
                    code="ASSET_NOT_FOUND",
                    message="Accepted candidate audio is missing from the project.",
                )
            clips.append(
                TimelineAudioClip(
                    segment_id=segment.id,
                    range=segment.range,
                    path=self._asset_path(project.id, audio_asset),
                )
            )
        if not clips:
            raise DomainError(
                code="INPUT_INVALID",
                message="Accept at least one generated candidate before rendering.",
                action="Generate and accept a candidate for a timeline segment.",
            )

        sample_rates = {sf.info(clip.path).samplerate for clip in clips}
        if len(sample_rates) != 1:
            raise DomainError(
                code="RENDER_FAILED",
                message="Accepted candidates must use one common sample rate for rendering.",
            )
        sample_rate = sample_rates.pop()
        references = {reference.id: reference for reference in project.voice_references}
        consents = {consent.id: consent for consent in project.consents}
        distribution_authorized = all(
            bool(
                consents.get(references[segment.voice_reference_id].consent_id)
                and consents[
                    references[segment.voice_reference_id].consent_id
                ].allow_generated_output_distribution
            )
            for segment in project.segments
            if segment.accepted_candidate_id is not None
        )
        output_dir = self.store.project_dir(project.id) / "exports" / f"revision-{project.revision}"
        dubbing_audio = output_dir / "dubbing.wav"
        try:
            assemble_dubbing_track(tuple(clips), dubbing_audio, sample_rate=sample_rate)
        except ValueError as error:
            raise DomainError(code="RENDER_FAILED", message=str(error)) from error

        source_video = next((asset for asset in project.assets if asset.kind == "video"), None)
        rendered_video: Path | None = None
        if source_video is not None:
            rendered_video = output_dir / "dubbed.mp4"
            try:
                mux_video(
                    self._asset_path(project.id, source_video),
                    dubbing_audio,
                    rendered_video,
                    mode=mode,
                )
            except RuntimeError as error:
                raise DomainError(
                    code="RENDER_FAILED",
                    message="FFmpeg could not mux the local video and accepted dubbing track.",
                    action=(
                        "Inspect the source video audio stream and retry with a compatible "
                        "mix mode."
                    ),
                    details={"error": str(error)},
                ) from error

        manifest = output_dir / "render.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    **asdict(
                        RenderResult(
                            dubbing_audio=dubbing_audio,
                            video=rendered_video,
                            manifest=manifest,
                            sample_rate=sample_rate,
                            mode=mode,
                            distribution_authorized=distribution_authorized,
                        )
                    ),
                    "content_label": AI_DUBBING_LABEL,
                    "mix_mode": mode,
                    "project_id": project.id,
                    "project_revision": project.revision,
                    "segments": [clip.segment_id for clip in clips],
                },
                default=str,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return RenderResult(
            dubbing_audio=dubbing_audio,
            video=rendered_video,
            manifest=manifest,
            sample_rate=sample_rate,
            mode=mode,
            distribution_authorized=distribution_authorized,
        )

    def _asset_path(self, project_id: str, asset: MediaAsset) -> Path:
        """Resolve a declared project asset while rejecting a path that escapes its asset root."""
        project_dir = self.store.project_dir(project_id)
        root = (project_dir / "assets").resolve()
        path = (project_dir / asset.relative_path).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise DomainError(code="ASSET_NOT_FOUND", message="Project asset data was not found.")
        return path
