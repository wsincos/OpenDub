"""Media assets, voice references, and authorization records."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from opendub.domain.ids import new_id, validate_uuid7
from opendub.domain.time import TimeRange

AssetKind = Literal["video", "audio", "image", "subtitle", "document"]
MaterialSource = Literal["self_recorded", "licensed", "public_domain", "authorized_other"]


class ConsentRecord(BaseModel):
    """A locally stored declaration that permits a voice reference's use."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    declaration_version: str = "v1"
    accepted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    material_source: MaterialSource
    authorization_purpose: str = Field(
        default="video_dubbing_generation", min_length=1, max_length=200
    )
    allow_generated_output_distribution: bool = False
    revision: int = Field(default=1, ge=1)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid7(value)


class MediaAsset(BaseModel):
    """Metadata for a content-addressed local asset, never a raw filesystem path."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    kind: AssetKind
    display_name: str = Field(min_length=1, max_length=255)
    relative_path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)
    duration_us: int | None = Field(default=None, gt=0)
    revision: int = Field(default=1, ge=1)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return validate_uuid7(value)


class VoiceReference(BaseModel):
    """An authorized audio source associated with one character voice."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(default_factory=new_id)
    asset_id: str
    range: TimeRange | None = None
    consent_id: str
    speaker_label: str = Field(min_length=1, max_length=200)
    revision: int = Field(default=1, ge=1)

    @field_validator("id", "asset_id", "consent_id")
    @classmethod
    def validate_ids(cls, value: str) -> str:
        return validate_uuid7(value)
