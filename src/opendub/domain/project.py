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
