"""Local-only HTTP application backed directly by the file project store."""

from __future__ import annotations

import base64
import binascii
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from opendub.domain.assets import (
    AssetKind,
    ConsentRecord,
    MaterialSource,
    MediaAsset,
    VoiceReference,
)
from opendub.domain.errors import DomainError
from opendub.domain.ids import new_id
from opendub.domain.project import Project
from opendub.domain.segments import DubbingSegment, EmotionLabel, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.registry import ModelRegistry, UpstreamModel
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


class CreateProjectRequest(BaseModel):
    """Validated request body for creating a new local project."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)


class UploadAssetRequest(BaseModel):
    """Upload a small local artifact through the loopback-only Studio API."""

    model_config = ConfigDict(extra="forbid")

    kind: AssetKind
    filename: str = Field(min_length=1, max_length=255)
    content_base64: str = Field(min_length=1, max_length=33_554_432)
    expected_revision: int = Field(ge=1)


class AssetMutationResult(MediaAsset):
    """An uploaded asset plus the project revision produced by the mutation."""

    project_revision: int = Field(ge=1)


class CreateVoiceReferenceRequest(BaseModel):
    """Create a local voice reference with an explicit material-rights declaration."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    speaker_label: str = Field(min_length=1, max_length=200)
    material_source: MaterialSource
    expected_revision: int = Field(ge=1)


class VoiceReferenceMutationResult(VoiceReference):
    """A newly registered voice reference and the resulting project revision."""

    project_revision: int = Field(ge=1)


class CreateSegmentRequest(BaseModel):
    """Create one configured timeline segment bound to an authorized voice reference."""

    model_config = ConfigDict(extra="forbid")

    start_us: int = Field(ge=0)
    end_us: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=10_000)
    language: str = Field(min_length=2, max_length=35)
    character_id: str | None = None
    voice_reference_id: str
    adapter_id: str = Field(min_length=1)
    emotion_label: EmotionLabel
    emotion_intensity: float = Field(ge=0.0, le=1.0)
    emotion_valence: float | None = Field(default=None, ge=-1.0, le=1.0)
    emotion_arousal: float | None = Field(default=None, ge=0.0, le=1.0)
    expected_revision: int = Field(ge=1)


class SegmentMutationResult(DubbingSegment):
    """A newly configured segment and the project revision produced by the mutation."""

    project_revision: int = Field(ge=1)


def create_app(*, workspace: Path | None = None) -> FastAPI:
    """Create an API application that defaults to a private local workspace."""
    root = (workspace or Path.cwd() / ".opendub").resolve()
    store = ProjectStore(root)
    artifacts = ArtifactStore(root)
    repository_root = Path(__file__).resolve().parents[3]
    model_registry = ModelRegistry(repository_root / "model-registry" / "upstreams.yaml")
    app = FastAPI(title="OpenDub Local API", version="0.0.1a0", docs_url="/api/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:5174",
            "http://localhost:5174",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "If-Match"],
    )

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "local"}

    @app.post("/api/v1/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
    def create_project(request: CreateProjectRequest) -> Project:
        return store.create(request.name)

    @app.get("/api/v1/projects/{project_id}", response_model=Project)
    def get_project(project_id: str) -> Project:
        try:
            return store.load(project_id)
        except DomainError as error:
            raise _http_error(error) from error

    @app.get("/api/v1/projects", response_model=tuple[Project, ...])
    def list_projects() -> tuple[Project, ...]:
        return store.iter_projects()

    @app.get("/api/v1/projects/{project_id}/assets/{asset_id}")
    def get_asset(project_id: str, asset_id: str) -> FileResponse:
        """Serve one recorded project asset without exposing arbitrary local paths."""
        try:
            project = store.load(project_id)
            asset = next((item for item in project.assets if item.id == asset_id), None)
            if asset is None:
                raise DomainError(code="ASSET_NOT_FOUND", message="Project asset was not found.")
            project_assets = (store.project_dir(project.id) / "assets").resolve()
            path = (store.project_dir(project.id) / asset.relative_path).resolve()
            if not path.is_relative_to(project_assets) or not path.is_file():
                raise DomainError(
                    code="ASSET_NOT_FOUND", message="Project asset data was not found."
                )
        except DomainError as error:
            raise _http_error(error) from error
        return FileResponse(path, filename=asset.display_name)

    @app.post(
        "/api/v1/projects/{project_id}/assets",
        response_model=AssetMutationResult,
        status_code=status.HTTP_201_CREATED,
    )
    def upload_asset(project_id: str, request: UploadAssetRequest) -> AssetMutationResult:
        """Store local asset bytes by content hash and attach its portable metadata."""
        try:
            data = base64.b64decode(request.content_base64, validate=True)
        except (ValueError, binascii.Error) as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail={
                    "code": "INPUT_INVALID",
                    "message": "content_base64 is not valid base64 data.",
                },
            ) from error
        suffix = Path(request.filename).suffix.lower().removeprefix(".")
        extension = suffix if suffix.isalnum() and len(suffix) <= 10 else "bin"
        try:
            project = store.load(project_id)
            if project.revision != request.expected_revision:
                raise DomainError(
                    code="PROJECT_CONFLICT",
                    message="Project was changed by another operation.",
                    action="Reload the project and retry the change.",
                )
            asset = artifacts.ingest_bytes(
                project.id,
                kind=request.kind,
                display_name=Path(request.filename).name,
                data=data,
                extension=extension,
            )
            updated = project.add_asset(asset, expected_revision=request.expected_revision)
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return AssetMutationResult(**asset.model_dump(), project_revision=updated.revision)

    @app.post(
        "/api/v1/projects/{project_id}/voice-references",
        response_model=VoiceReferenceMutationResult,
        status_code=status.HTTP_201_CREATED,
    )
    def create_voice_reference(
        project_id: str, request: CreateVoiceReferenceRequest
    ) -> VoiceReferenceMutationResult:
        """Bind an audio asset to one speaker only after recording an authorization declaration."""
        try:
            project = store.load(project_id)
            consent = ConsentRecord(material_source=request.material_source)
            reference = VoiceReference(
                asset_id=request.asset_id,
                consent_id=consent.id,
                speaker_label=request.speaker_label,
            )
            updated = project.add_voice_reference(
                consent, reference, expected_revision=request.expected_revision
            )
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return VoiceReferenceMutationResult(
            **reference.model_dump(), project_revision=updated.revision
        )

    @app.post(
        "/api/v1/projects/{project_id}/segments",
        response_model=SegmentMutationResult,
        status_code=status.HTTP_201_CREATED,
    )
    def create_segment(project_id: str, request: CreateSegmentRequest) -> SegmentMutationResult:
        """Create a ready-to-generate line on the project's microsecond timeline."""
        try:
            project = store.load(project_id)
            segment = DubbingSegment(
                id=new_id(),
                range=TimeRange(start_us=request.start_us, end_us=request.end_us),
                text=request.text,
                language=request.language,
                character_id=request.character_id or new_id(),
                voice_reference_id=request.voice_reference_id,
                emotion=EmotionSpec(
                    label=request.emotion_label,
                    intensity=request.emotion_intensity,
                    valence=request.emotion_valence,
                    arousal=request.emotion_arousal,
                ),
                adapter_id=request.adapter_id,
                status="ready",
            )
            updated = project.add_segment(segment, expected_revision=request.expected_revision)
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return SegmentMutationResult(**segment.model_dump(), project_revision=updated.revision)

    @app.get("/api/v1/models", response_model=tuple[UpstreamModel, ...])
    def list_models() -> tuple[UpstreamModel, ...]:
        return model_registry.discover()

    return app


def _http_error(error: DomainError) -> HTTPException:
    status_code = (
        status.HTTP_409_CONFLICT if error.code == "PROJECT_CONFLICT" else status.HTTP_404_NOT_FOUND
    )
    return HTTPException(
        status_code=status_code,
        detail={"code": error.code, "message": error.message, "action": error.action},
    )


app = create_app()
