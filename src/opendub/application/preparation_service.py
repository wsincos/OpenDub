"""Validate and export a local, evidence-bound project preparation record."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from opendub.domain.assets import InputAuthorization, MediaAsset
from opendub.domain.errors import DomainError
from opendub.domain.project import Project
from opendub.domain.segments import DubbingSegment
from opendub.domain.time import TimeRange
from opendub.storage.atomic import atomic_write_text
from opendub.storage.project_store import ProjectStore


@dataclass(frozen=True)
class PreparationExportResult:
    """The local path and immutable revision represented by one preparation export."""

    manifest: Path
    project_revision: int


class PreparationService:
    """Create a portable record only when a project satisfies the preparation contract."""

    def __init__(self, store: ProjectStore) -> None:
        self.store = store

    def export(self, project_id: str) -> PreparationExportResult:
        """Write the current validated project state without copying any media bytes."""
        project = self.store.load(project_id)
        video, video_authorization, text_authorization = self._validate(project)
        selection = project.method_selection
        assert selection is not None
        voice_references = {reference.id: reference for reference in project.voice_references}
        consents = {consent.id: consent for consent in project.consents}
        assets = {asset.id: asset for asset in project.assets}
        manifest = (
            self.store.project_dir(project.id)
            / "preparation"
            / (f"revision-{project.revision}")
            / "preparation.json"
        )
        payload = {
            "schema_version": "opendub.project-preparation/v1",
            "content_label": "OpenDub local project preparation record",
            "project": {
                "id": project.id,
                "name": project.name,
                "revision": project.revision,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            },
            "method_selection": selection.model_dump(mode="json"),
            "inputs": {
                "video": {
                    **_asset_record(video),
                    "authorization": video_authorization.model_dump(mode="json"),
                },
                "target_text": {
                    "sha256": target_text_fingerprint(project.segments),
                    "authorization": text_authorization.model_dump(mode="json"),
                },
                "reference_speech": [
                    {
                        "reference_id": reference.id,
                        "speaker_label": reference.speaker_label,
                        "range": _range_record(reference.range) if reference.range else None,
                        "asset": _asset_record(assets[reference.asset_id]),
                        "consent_id": consents[reference.consent_id].id,
                        "consent": consents[reference.consent_id].model_dump(mode="json"),
                    }
                    for reference in sorted(
                        (
                            voice_references[segment.voice_reference_id]
                            for segment in project.segments
                        ),
                        key=lambda item: item.id,
                    )
                ],
            },
            "segments": [
                {
                    "id": segment.id,
                    "range": _range_record(segment.range),
                    "text": segment.text,
                    "language": segment.language,
                    "character_id": segment.character_id,
                    "voice_reference_id": segment.voice_reference_id,
                    "emotion": segment.emotion.model_dump(mode="json"),
                    "adapter_id": segment.adapter_id,
                    "revision": segment.revision,
                }
                for segment in project.segments
            ],
            "runtime": {
                "status": selection.runtime_status,
                "content_modes": selection.content_modes,
                "live_admitted": _is_live_admitted(project),
            },
        }
        atomic_write_text(
            manifest,
            json.dumps(payload, default=str, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        return PreparationExportResult(manifest=manifest, project_revision=project.revision)

    def _validate(
        self, project: Project
    ) -> tuple[MediaAsset, InputAuthorization, InputAuthorization]:
        if project.method_selection is None:
            raise DomainError(
                code="INPUT_INVALID",
                message="Select one complete method before exporting a preparation record.",
            )
        if not project.segments:
            raise DomainError(
                code="INPUT_INVALID",
                message="Add at least one target-text timeline segment before exporting.",
            )
        mismatched_segments = [
            segment.id
            for segment in project.segments
            if segment.adapter_id != project.method_selection.method_id
        ]
        if mismatched_segments:
            raise DomainError(
                code="INPUT_INVALID",
                message="Every timeline segment must use the selected complete method.",
                details={"segment_ids": mismatched_segments},
            )

        assets = {asset.id: asset for asset in project.assets}
        videos = [asset for asset in project.assets if asset.kind == "video"]
        video_authorizations = [
            authorization
            for authorization in project.input_authorizations
            if authorization.input_kind == "video"
            and authorization.asset_id in assets
            and assets[authorization.asset_id].kind == "video"
            and assets[authorization.asset_id].sha256 == authorization.content_sha256
        ]
        authorized_videos = [
            asset
            for asset in videos
            if any(authorization.asset_id == asset.id for authorization in video_authorizations)
        ]
        if len(authorized_videos) != 1:
            raise DomainError(
                code="RIGHTS_DECLARATION_REQUIRED",
                message="Record exactly one current video authorization before exporting.",
            )
        video = authorized_videos[0]
        video_authorization = next(
            authorization
            for authorization in reversed(video_authorizations)
            if authorization.asset_id == video.id
        )

        text_hash = target_text_fingerprint(project.segments)
        text_authorization = next(
            (
                authorization
                for authorization in reversed(project.input_authorizations)
                if authorization.input_kind == "target_text"
                and authorization.content_sha256 == text_hash
            ),
            None,
        )
        if text_authorization is None:
            raise DomainError(
                code="RIGHTS_DECLARATION_REQUIRED",
                message="Record a current target text authorization before exporting.",
            )

        references = {reference.id: reference for reference in project.voice_references}
        consents = {consent.id: consent for consent in project.consents}
        missing_reference_records = [
            segment.id
            for segment in project.segments
            if segment.voice_reference_id not in references
            or references[segment.voice_reference_id].asset_id not in assets
            or references[segment.voice_reference_id].consent_id not in consents
        ]
        if missing_reference_records:
            raise DomainError(
                code="RIGHTS_DECLARATION_REQUIRED",
                message="Every target-text segment needs an authorized reference speech record.",
                details={"segment_ids": missing_reference_records},
            )
        return video, video_authorization, text_authorization


def target_text_fingerprint(segments: tuple[DubbingSegment, ...]) -> str:
    """Hash the normalized editable text state that an authorization covers."""
    normalized = [
        {
            "id": segment.id,
            "text": segment.text,
            "language": segment.language,
            "start_us": segment.range.start_us,
            "end_us": segment.range.end_us,
        }
        for segment in segments
    ]
    encoded = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _asset_record(asset: MediaAsset) -> dict[str, object]:
    return {
        "asset_id": asset.id,
        "display_name": asset.display_name,
        "kind": asset.kind,
        "sha256": asset.sha256,
        "size_bytes": asset.size_bytes,
        "duration_us": asset.duration_us,
    }


def _range_record(time_range: TimeRange) -> dict[str, int]:
    """Serialize the small immutable timeline value without coupling it to Pydantic."""
    return {"start_us": time_range.start_us, "end_us": time_range.end_us}


def _is_live_admitted(project: Project) -> bool:
    selection = project.method_selection
    return bool(
        selection
        and selection.runtime_status in {"experimental", "stable"}
        and "live" in selection.content_modes
    )
