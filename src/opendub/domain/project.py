"""The top-level, versioned project aggregate and consistency operations."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from opendub.domain.assets import ConsentRecord, MediaAsset, VoiceReference
from opendub.domain.candidates import Candidate
from opendub.domain.errors import DomainError
from opendub.domain.ids import new_id, validate_uuid7
from opendub.domain.segments import DubbingSegment


class Project(BaseModel):
    """The file-backed source of truth for an OpenDub project."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = "opendub.project/v1"
    id: str = Field(default_factory=new_id)
    name: str = Field(min_length=1, max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revision: int = Field(default=1, ge=1)
    consents: tuple[ConsentRecord, ...] = ()
    assets: tuple[MediaAsset, ...] = ()
    voice_references: tuple[VoiceReference, ...] = ()
    segments: tuple[DubbingSegment, ...] = ()
    candidates: tuple[Candidate, ...] = ()

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid7(value)

    def accept_candidate(
        self,
        segment_id: str,
        candidate_id: str,
        expected_revision: int,
    ) -> Project:
        """Accept a current candidate using optimistic concurrency control."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )

        segment = next((item for item in self.segments if item.id == segment_id), None)
        candidate = next((item for item in self.candidates if item.id == candidate_id), None)
        if segment is None or candidate is None or candidate.segment_id != segment_id:
            raise DomainError(
                code="INPUT_INVALID",
                message="Candidate does not belong to the segment.",
            )
        if candidate.segment_revision != segment.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Candidate was generated for an earlier segment revision.",
                action="Generate a new candidate for the current segment.",
            )
        if segment.status == "unconfigured":
            raise DomainError(
                code="INPUT_INVALID",
                message="Segment must be configured before acceptance.",
            )

        accepted = segment.model_copy(
            update={
                "accepted_candidate_id": candidate.id,
                "status": "accepted",
                "revision": segment.revision + 1,
            }
        )
        segments = tuple(accepted if item.id == segment.id else item for item in self.segments)
        return self.model_copy(
            update={
                "segments": segments,
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def add_segment(self, segment: DubbingSegment, expected_revision: int) -> Project:
        """Append a uniquely identified segment using optimistic concurrency control."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        if any(item.id == segment.id for item in self.segments):
            raise DomainError(code="INPUT_INVALID", message="Segment identifier is already in use.")
        if not any(
            reference.id == segment.voice_reference_id for reference in self.voice_references
        ):
            raise DomainError(
                code="ASSET_NOT_FOUND",
                message="Segment must reference an authorized voice reference in this project.",
            )
        return self.model_copy(
            update={
                "segments": (*self.segments, segment),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def add_segments(
        self, segments_to_add: tuple[DubbingSegment, ...], expected_revision: int
    ) -> Project:
        """Append a subtitle-derived batch as one revisioned project change."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        ids = [segment.id for segment in segments_to_add]
        if len(ids) != len(set(ids)) or any(item.id in ids for item in self.segments):
            raise DomainError(code="INPUT_INVALID", message="Segment identifier is already in use.")
        reference_ids = {reference.id for reference in self.voice_references}
        if any(segment.voice_reference_id not in reference_ids for segment in segments_to_add):
            raise DomainError(
                code="ASSET_NOT_FOUND",
                message=(
                    "Every segment must reference an authorized voice reference in this project."
                ),
            )
        return self.model_copy(
            update={
                "segments": (*self.segments, *segments_to_add),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def update_segment(self, segment: DubbingSegment, expected_revision: int) -> Project:
        """Update a segment and invalidate any candidate that targets its old revision."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        previous = next((item for item in self.segments if item.id == segment.id), None)
        if previous is None:
            raise DomainError(code="ASSET_NOT_FOUND", message="Dubbing segment was not found.")
        if not any(
            reference.id == segment.voice_reference_id for reference in self.voice_references
        ):
            raise DomainError(
                code="ASSET_NOT_FOUND",
                message="Segment must reference an authorized voice reference in this project.",
            )
        updated_segment = segment.model_copy(
            update={
                "status": "ready",
                "accepted_candidate_id": None,
                "revision": previous.revision + 1,
            }
        )
        segments = tuple(
            updated_segment if item.id == segment.id else item for item in self.segments
        )
        return self.model_copy(
            update={
                "segments": segments,
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def remove_segment(self, segment_id: str, expected_revision: int) -> Project:
        """Remove a timeline segment and candidate records without deleting audio artifacts."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        if not any(item.id == segment_id for item in self.segments):
            raise DomainError(code="ASSET_NOT_FOUND", message="Dubbing segment was not found.")
        return self.model_copy(
            update={
                "segments": tuple(item for item in self.segments if item.id != segment_id),
                "candidates": tuple(
                    item for item in self.candidates if item.segment_id != segment_id
                ),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def add_asset(self, asset: MediaAsset, expected_revision: int) -> Project:
        """Attach a content-addressed local asset using optimistic concurrency control."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        if any(item.id == asset.id for item in self.assets):
            raise DomainError(code="INPUT_INVALID", message="Asset identifier is already in use.")
        return self.model_copy(
            update={
                "assets": (*self.assets, asset),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def add_voice_reference(
        self,
        consent: ConsentRecord,
        reference: VoiceReference,
        expected_revision: int,
    ) -> Project:
        """Register an authorized voice reference backed by an existing audio asset."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        asset = next((item for item in self.assets if item.id == reference.asset_id), None)
        if asset is None or asset.kind != "audio":
            raise DomainError(
                code="ASSET_NOT_FOUND",
                message="Voice reference must use an audio asset in this project.",
            )
        if reference.consent_id != consent.id:
            raise DomainError(
                code="RIGHTS_DECLARATION_REQUIRED",
                message="Voice reference must be linked to its explicit consent declaration.",
            )
        if any(item.id == reference.id for item in self.voice_references):
            raise DomainError(
                code="INPUT_INVALID", message="Voice reference identifier is already in use."
            )
        if any(item.id == consent.id for item in self.consents):
            raise DomainError(code="INPUT_INVALID", message="Consent identifier is already in use.")
        return self.model_copy(
            update={
                "consents": (*self.consents, consent),
                "voice_references": (*self.voice_references, reference),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )

    def record_generated_candidate(
        self,
        candidate: Candidate,
        audio_asset: MediaAsset,
        expected_revision: int,
    ) -> Project:
        """Attach a current generated candidate and advance its segment revision."""
        if expected_revision != self.revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        segment = next((item for item in self.segments if item.id == candidate.segment_id), None)
        if segment is None or candidate.audio_asset_id != audio_asset.id:
            raise DomainError(
                code="INPUT_INVALID",
                message="Candidate references an invalid project resource.",
            )
        if candidate.segment_revision != segment.revision + 1:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Candidate does not target the next segment revision.",
            )
        generated_segment = segment.model_copy(
            update={"status": "generated", "revision": candidate.segment_revision}
        )
        segments = tuple(
            generated_segment if item.id == segment.id else item for item in self.segments
        )
        return self.model_copy(
            update={
                "assets": (*self.assets, audio_asset),
                "segments": segments,
                "candidates": (*self.candidates, candidate),
                "revision": self.revision + 1,
                "updated_at": datetime.now(UTC),
            }
        )
