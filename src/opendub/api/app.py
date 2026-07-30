"""Local-only HTTP application backed directly by the file project store."""

from __future__ import annotations

import base64
import binascii
import json
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from opendub.application.evaluation_service import EvaluationService
from opendub.application.ingest_service import segments_from_subtitles
from opendub.application.preparation_service import PreparationService, target_text_fingerprint
from opendub.application.render_service import RenderService
from opendub.atlas.models import AtlasValidationError, MethodManifest
from opendub.domain.assets import (
    AssetKind,
    ConsentRecord,
    InputAuthorization,
    InputKind,
    MaterialSource,
    MediaAsset,
    VoiceReference,
)
from opendub.domain.errors import DomainError
from opendub.domain.ids import new_id
from opendub.domain.metrics import MetricResult
from opendub.domain.project import MethodSelection, Project
from opendub.domain.segments import DubbingSegment, EmotionLabel, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.jobs.models import JobEvent, JobRecord
from opendub.jobs.repository import JobRepository
from opendub.media.probe import probe_media
from opendub.media.timeline import import_srt, import_vtt
from opendub.models.registry import ModelRegistry, UpstreamModel
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


class CreateProjectRequest(BaseModel):
    """Validated request body for creating a new local project."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)


class SelectMethodRequest(MethodSelection):
    """Persist an evidence-bound complete-method choice for one local project."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=1)


class InputAuthorizationRequest(BaseModel):
    """Record local use authorization for the project video or current target text."""

    model_config = ConfigDict(extra="forbid")

    input_kind: InputKind
    asset_id: str | None = None
    material_source: MaterialSource
    authorization_purpose: str = Field(
        default="video_dubbing_project_preparation", min_length=1, max_length=200
    )
    expected_revision: int = Field(ge=1)


class InputAuthorizationMutationResult(InputAuthorization):
    """An input authorization together with the revision it created."""

    project_revision: int = Field(ge=1)


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
    authorization_purpose: str = Field(
        default="video_dubbing_generation", min_length=1, max_length=200
    )
    allow_generated_output_distribution: bool = False
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


class AcceptCandidateRequest(BaseModel):
    """Accept a current candidate with the revision that was reviewed."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=1)


class UpdateSegmentRequest(BaseModel):
    """Apply explicit changes to a timeline segment at the revision being edited."""

    model_config = ConfigDict(extra="forbid")

    text: str | None = Field(default=None, min_length=1, max_length=10_000)
    start_us: int | None = Field(default=None, ge=0)
    end_us: int | None = Field(default=None, gt=0)
    language: str | None = Field(default=None, min_length=2, max_length=35)
    character_id: str | None = None
    voice_reference_id: str | None = None
    adapter_id: str | None = Field(default=None, min_length=1)
    emotion_label: EmotionLabel | None = None
    emotion_intensity: float | None = Field(default=None, ge=0.0, le=1.0)
    emotion_valence: float | None = Field(default=None, ge=-1.0, le=1.0)
    emotion_arousal: float | None = Field(default=None, ge=0.0, le=1.0)
    expected_revision: int = Field(ge=1)


class ImportSubtitlesRequest(BaseModel):
    """Map an in-project SRT or VTT asset to ready timeline segments."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    language: str = Field(min_length=2, max_length=35)
    character_id: str | None = None
    voice_reference_id: str
    adapter_id: str = Field(min_length=1)
    emotion_label: EmotionLabel = "neutral"
    emotion_intensity: float = Field(default=0.5, ge=0.0, le=1.0)
    expected_revision: int = Field(ge=1)


class DeleteSegmentRequest(BaseModel):
    """Remove a segment using the project revision shown to the user."""

    model_config = ConfigDict(extra="forbid")

    expected_revision: int = Field(ge=1)


RenderMixMode = Literal["preserve", "duck", "remove"]


class RenderRequest(BaseModel):
    """Render the current accepted local candidates with an explicit audio policy."""

    model_config = ConfigDict(extra="forbid")

    mix_mode: RenderMixMode = "remove"


class RenderResponse(BaseModel):
    """Local-only export locations for a deterministic project revision render."""

    project_id: str
    project_revision: int = Field(ge=1)
    mix_mode: RenderMixMode
    sample_rate: int = Field(gt=0)
    distribution_authorized: bool
    dubbing_audio_url: str
    dubbed_video_url: str | None
    manifest_url: str


class PreparationExportResponse(BaseModel):
    """A safe local URL for one validated project-preparation record."""

    project_id: str
    project_revision: int = Field(ge=1)
    manifest_url: str


class EvaluationResponse(BaseModel):
    """Locations and truthful metric records for one local candidate evaluation."""

    candidate_id: str
    metrics: tuple[MetricResult, ...]
    report_json_url: str
    report_markdown_url: str


def create_app(*, workspace: Path | None = None) -> FastAPI:
    """Create an API application that defaults to a private local workspace."""
    root = (workspace or Path.cwd() / ".opendub").resolve()
    store = ProjectStore(root)
    jobs = JobRepository(root / "jobs.json")
    artifacts = ArtifactStore(root)
    repository_root = Path(__file__).resolve().parents[3]
    model_registry = ModelRegistry(repository_root / "config" / "model-registry" / "upstreams.yaml")
    app = FastAPI(title="OpenDub Local API", version="0.4.0", docs_url="/api/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:5174",
            "http://localhost:5174",
        ],
        allow_origin_regex=r"^http://(?:127\.0\.0\.1|localhost):[0-9]+$",
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
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

    @app.put("/api/v1/projects/{project_id}/method-selection", response_model=Project)
    def select_method(project_id: str, request: SelectMethodRequest) -> Project:
        """Save one complete-method choice without claiming a Live model run."""
        try:
            project = store.load(project_id)
            selection = MethodSelection(**request.model_dump(exclude={"expected_revision"}))
            _validate_method_selection_evidence(
                selection, content_root=repository_root / "apps" / "web" / "content"
            )
            updated = project.select_method(selection, expected_revision=request.expected_revision)
            return store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error

    @app.post(
        "/api/v1/projects/{project_id}/input-authorizations",
        response_model=InputAuthorizationMutationResult,
        status_code=status.HTTP_201_CREATED,
    )
    def authorize_project_input(
        project_id: str, request: InputAuthorizationRequest
    ) -> InputAuthorizationMutationResult:
        """Bind a video asset or exact target text state to an explicit local declaration."""
        try:
            project = store.load(project_id)
            if request.input_kind == "video":
                asset = next((item for item in project.assets if item.id == request.asset_id), None)
                if asset is None or asset.kind != "video":
                    raise DomainError(
                        code="ASSET_NOT_FOUND",
                        message="Choose a project video before recording its authorization.",
                    )
                content_sha256 = asset.sha256
            else:
                if request.asset_id is not None:
                    raise DomainError(
                        code="INPUT_INVALID",
                        message="Target text authorization cannot reference a media asset.",
                    )
                content_sha256 = target_text_fingerprint(project.segments)
            authorization = InputAuthorization(
                input_kind=request.input_kind,
                asset_id=request.asset_id,
                content_sha256=content_sha256,
                material_source=request.material_source,
                authorization_purpose=request.authorization_purpose,
            )
            updated = project.authorize_input(
                authorization, expected_revision=request.expected_revision
            )
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return InputAuthorizationMutationResult(
            **authorization.model_dump(), project_revision=updated.revision
        )

    @app.post(
        "/api/v1/projects/{project_id}/preparation-export",
        response_model=PreparationExportResponse,
    )
    def export_project_preparation(project_id: str) -> PreparationExportResponse:
        """Export the current selected-method preparation record without running a model."""
        try:
            result = PreparationService(store).export(project_id)
        except DomainError as error:
            raise _http_error(error) from error
        export_root = (
            f"/api/v1/projects/{project_id}/preparation-exports/revision-{result.project_revision}"
        )
        return PreparationExportResponse(
            project_id=project_id,
            project_revision=result.project_revision,
            manifest_url=f"{export_root}/preparation.json",
        )

    @app.get("/api/v1/projects/{project_id}/jobs", response_model=tuple[JobRecord, ...])
    def list_project_jobs(project_id: str) -> tuple[JobRecord, ...]:
        """List the durable local job ledger entries belonging to one project."""
        try:
            store.load(project_id)
        except DomainError as error:
            raise _http_error(error) from error
        return jobs.list(project_id=project_id)

    @app.get("/api/v1/jobs/{job_id}", response_model=JobRecord)
    def get_job(job_id: str) -> JobRecord:
        """Return one durable job state without disclosing project filesystem paths."""
        try:
            return jobs.get(job_id)
        except DomainError as error:
            raise _http_error(error) from error

    @app.get("/api/v1/jobs/{job_id}/events")
    def replay_job_events(
        job_id: str,
        after_id: int = Query(default=0, ge=0),
    ) -> StreamingResponse:
        """Replay the persisted suffix of a job's progress events as Server-Sent Events."""
        try:
            events = jobs.events(job_id, after_id=after_id)
        except DomainError as error:
            raise _http_error(error) from error
        return StreamingResponse(
            _sse_events(events),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

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
            duration_us = _validated_upload_duration(
                data=data,
                extension=extension,
                kind=request.kind,
                project_root=store.project_dir(project.id),
            )
            asset = artifacts.ingest_bytes(
                project.id,
                kind=request.kind,
                display_name=Path(request.filename).name,
                data=data,
                extension=extension,
            )
            if duration_us is not None:
                asset = asset.model_copy(update={"duration_us": duration_us})
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
            consent = ConsentRecord(
                material_source=request.material_source,
                authorization_purpose=request.authorization_purpose,
                allow_generated_output_distribution=request.allow_generated_output_distribution,
            )
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

    @app.patch(
        "/api/v1/projects/{project_id}/segments/{segment_id}",
        response_model=SegmentMutationResult,
    )
    def update_segment(
        project_id: str, segment_id: str, request: UpdateSegmentRequest
    ) -> SegmentMutationResult:
        """Edit one line while invalidating candidates for the old segment revision."""
        try:
            project = store.load(project_id)
            current = next((item for item in project.segments if item.id == segment_id), None)
            if current is None:
                raise DomainError(code="ASSET_NOT_FOUND", message="Dubbing segment was not found.")
            time_range = TimeRange(
                start_us=request.start_us
                if request.start_us is not None
                else current.range.start_us,
                end_us=request.end_us if request.end_us is not None else current.range.end_us,
            )
            emotion = EmotionSpec(
                label=request.emotion_label or current.emotion.label,
                intensity=(
                    request.emotion_intensity
                    if request.emotion_intensity is not None
                    else current.emotion.intensity
                ),
                valence=(
                    request.emotion_valence
                    if request.emotion_valence is not None
                    else current.emotion.valence
                ),
                arousal=(
                    request.emotion_arousal
                    if request.emotion_arousal is not None
                    else current.emotion.arousal
                ),
            )
            segment = current.model_copy(
                update={
                    "range": time_range,
                    "text": request.text or current.text,
                    "language": request.language or current.language,
                    "character_id": request.character_id or current.character_id,
                    "voice_reference_id": request.voice_reference_id or current.voice_reference_id,
                    "adapter_id": request.adapter_id or current.adapter_id,
                    "emotion": emotion,
                }
            )
            updated = project.update_segment(segment, expected_revision=request.expected_revision)
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        persisted = next(item for item in updated.segments if item.id == segment_id)
        return SegmentMutationResult(**persisted.model_dump(), project_revision=updated.revision)

    @app.post("/api/v1/projects/{project_id}/segments/import-subtitles", response_model=Project)
    def import_subtitles(project_id: str, request: ImportSubtitlesRequest) -> Project:
        """Create ready segments from an already local, validated subtitle asset."""
        try:
            project = store.load(project_id)
            asset = next((item for item in project.assets if item.id == request.asset_id), None)
            if asset is None or asset.kind != "subtitle":
                raise DomainError(code="ASSET_NOT_FOUND", message="Subtitle asset was not found.")
            asset_path = _project_asset_path(store, project, asset)
            importer = import_vtt if asset_path.suffix.lower() == ".vtt" else import_srt
            cues = importer(asset_path)
            if not cues:
                raise DomainError(
                    code="INPUT_INVALID", message="Subtitle asset has no importable cues."
                )
            segments = segments_from_subtitles(
                cues,
                language=request.language,
                character_id=request.character_id or new_id(),
                voice_reference_id=request.voice_reference_id,
                adapter_id=request.adapter_id,
                emotion=EmotionSpec(
                    label=request.emotion_label, intensity=request.emotion_intensity
                ),
            )
            updated = project.add_segments(segments, expected_revision=request.expected_revision)
            store.save(updated, expected_revision=request.expected_revision)
        except (DomainError, ValueError) as error:
            if isinstance(error, DomainError):
                raise _http_error(error) from error
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail={"code": "INPUT_INVALID", "message": str(error)},
            ) from error
        return updated

    @app.delete("/api/v1/projects/{project_id}/segments/{segment_id}", response_model=Project)
    def delete_segment(project_id: str, segment_id: str, request: DeleteSegmentRequest) -> Project:
        """Remove one segment and its candidate records with optimistic concurrency control."""
        try:
            project = store.load(project_id)
            updated = project.remove_segment(
                segment_id, expected_revision=request.expected_revision
            )
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return updated

    @app.post(
        "/api/v1/projects/{project_id}/segments/{segment_id}/candidates/{candidate_id}/accept",
        response_model=Project,
    )
    def accept_candidate(
        project_id: str,
        segment_id: str,
        candidate_id: str,
        request: AcceptCandidateRequest,
    ) -> Project:
        """Commit a reviewed current candidate without accepting stale output."""
        try:
            project = store.load(project_id)
            updated = project.accept_candidate(
                segment_id, candidate_id, expected_revision=request.expected_revision
            )
            store.save(updated, expected_revision=request.expected_revision)
        except DomainError as error:
            raise _http_error(error) from error
        return updated

    @app.post(
        "/api/v1/projects/{project_id}/renders",
        response_model=RenderResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def render_project(project_id: str, request: RenderRequest) -> RenderResponse:
        """Render only candidates explicitly accepted at the current project revision."""
        try:
            result = RenderService(store).render(project_id, mode=request.mix_mode)
            project = store.load(project_id)
        except DomainError as error:
            raise _http_error(error) from error

        export_root = f"/api/v1/projects/{project.id}/exports/revision-{project.revision}"
        return RenderResponse(
            project_id=project.id,
            project_revision=project.revision,
            mix_mode=request.mix_mode,
            sample_rate=result.sample_rate,
            distribution_authorized=result.distribution_authorized,
            dubbing_audio_url=f"{export_root}/dubbing.wav",
            dubbed_video_url=(f"{export_root}/dubbed.mp4" if result.video is not None else None),
            manifest_url=f"{export_root}/render.json",
        )

    @app.get("/api/v1/projects/{project_id}/exports/{export_directory}/{artifact}")
    def get_export(project_id: str, export_directory: str, artifact: str) -> FileResponse:
        """Serve only a named local render artifact from a declared revision directory."""
        allowed_artifacts = {"dubbing.wav", "dubbed.mp4", "render.json"}
        if (
            not export_directory.startswith("revision-")
            or not export_directory.removeprefix("revision-").isdigit()
            or artifact not in allowed_artifacts
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        try:
            project = store.load(project_id)
            export_root = (store.project_dir(project.id) / "exports").resolve()
            path = (export_root / export_directory / artifact).resolve()
            if not path.is_relative_to(export_root) or not path.is_file():
                raise DomainError(code="ASSET_NOT_FOUND", message="Render artifact was not found.")
        except DomainError as error:
            raise _http_error(error) from error
        return FileResponse(path, filename=artifact)

    @app.get("/api/v1/projects/{project_id}/preparation-exports/{export_directory}/{artifact}")
    def get_preparation_export(
        project_id: str, export_directory: str, artifact: str
    ) -> FileResponse:
        """Serve a fixed local preparation record without exposing arbitrary project files."""
        if (
            not export_directory.startswith("revision-")
            or not export_directory.removeprefix("revision-").isdigit()
            or artifact != "preparation.json"
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        try:
            project = store.load(project_id)
            preparation_root = (store.project_dir(project.id) / "preparation").resolve()
            path = (preparation_root / export_directory / artifact).resolve()
            if not path.is_relative_to(preparation_root) or not path.is_file():
                raise DomainError(
                    code="ASSET_NOT_FOUND", message="Preparation record was not found."
                )
        except DomainError as error:
            raise _http_error(error) from error
        return FileResponse(path, filename=artifact)

    @app.post(
        "/api/v1/projects/{project_id}/candidates/{candidate_id}/evaluate",
        response_model=EvaluationResponse,
    )
    def evaluate_candidate(project_id: str, candidate_id: str) -> EvaluationResponse:
        """Calculate deterministic audio metrics and record unavailable neural metrics honestly."""
        try:
            report = EvaluationService(store).evaluate_candidate(project_id, candidate_id)
            project = store.load(project_id)
            candidate = next(item for item in project.candidates if item.id == candidate_id)
        except DomainError as error:
            raise _http_error(error) from error
        report_root = f"/api/v1/projects/{project.id}/reports/{candidate.id}/r{candidate.revision}"
        return EvaluationResponse(
            candidate_id=candidate.id,
            metrics=report.metrics,
            report_json_url=f"{report_root}/evaluation.json",
            report_markdown_url=f"{report_root}/evaluation.md",
        )

    @app.get("/api/v1/projects/{project_id}/reports/{candidate_id}/{report_revision}/{artifact}")
    def get_report(
        project_id: str, candidate_id: str, report_revision: str, artifact: str
    ) -> FileResponse:
        """Serve only fixed evaluation artifacts for a declared candidate revision."""
        if (
            not report_revision.startswith("r")
            or not report_revision.removeprefix("r").isdigit()
            or artifact not in {"evaluation.json", "evaluation.md"}
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        try:
            project = store.load(project_id)
            candidate = next((item for item in project.candidates if item.id == candidate_id), None)
            if candidate is None or report_revision != f"r{candidate.revision}":
                raise DomainError(
                    code="ASSET_NOT_FOUND", message="Evaluation report was not found."
                )
            reports_root = (store.project_dir(project.id) / "reports").resolve()
            path = (reports_root / candidate.id / report_revision / artifact).resolve()
            if not path.is_relative_to(reports_root) or not path.is_file():
                raise DomainError(
                    code="ASSET_NOT_FOUND", message="Evaluation report was not found."
                )
        except DomainError as error:
            raise _http_error(error) from error
        return FileResponse(path, filename=artifact)

    @app.get("/api/v1/models", response_model=tuple[UpstreamModel, ...])
    def list_models() -> tuple[UpstreamModel, ...]:
        return model_registry.discover()

    return app


def _validated_upload_duration(
    *,
    data: bytes,
    extension: str,
    kind: AssetKind,
    project_root: Path,
) -> int | None:
    """Probe user-supplied audio/video before it becomes a declared project asset."""
    if kind not in {"audio", "video"}:
        return None
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=project_root,
            prefix=".upload-",
            suffix=f".{extension}",
            delete=False,
        ) as temporary:
            temporary.write(data)
            temporary_path = Path(temporary.name)
        probe = probe_media(temporary_path)
    except (OSError, RuntimeError, ValueError) as error:
        raise DomainError(
            code="INPUT_INVALID",
            message="The uploaded file is not a readable media asset.",
            action="Choose an audio or video file that FFprobe can inspect.",
        ) from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    if kind == "audio" and probe.audio_sample_rate is None:
        raise DomainError(
            code="INPUT_INVALID",
            message="The uploaded audio asset has no readable audio stream.",
        )
    if kind == "video" and probe.video_width is None:
        raise DomainError(
            code="INPUT_INVALID",
            message="The uploaded video asset has no readable video stream.",
        )
    return probe.duration_us


def _http_error(error: DomainError) -> HTTPException:
    status_code_by_error = {
        "ASSET_NOT_FOUND": status.HTTP_404_NOT_FOUND,
        "PROJECT_CONFLICT": status.HTTP_409_CONFLICT,
        "INPUT_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "RIGHTS_DECLARATION_REQUIRED": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "RENDER_FAILED": status.HTTP_422_UNPROCESSABLE_CONTENT,
    }
    status_code = status_code_by_error.get(error.code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HTTPException(
        status_code=status_code,
        detail={"code": error.code, "message": error.message, "action": error.action},
    )


def _project_asset_path(store: ProjectStore, project: Project, asset: MediaAsset) -> Path:
    """Resolve one project asset without allowing a corrupted manifest to escape its asset root."""
    project_assets = (store.project_dir(project.id) / "assets").resolve()
    path = (store.project_dir(project.id) / asset.relative_path).resolve()
    if not path.is_relative_to(project_assets) or not path.is_file():
        raise DomainError(code="ASSET_NOT_FOUND", message="Project asset data was not found.")
    return path


def _validate_method_selection_evidence(selection: MethodSelection, *, content_root: Path) -> None:
    """Bind persisted selection status and commit to the local validated Method Manifest."""
    slug = selection.method_id.rsplit("/", maxsplit=1)[-1]
    manifest_path = content_root / "methods" / slug / "method.json"
    try:
        manifest = MethodManifest.model_validate(
            json.loads(manifest_path.read_text(encoding="utf-8"))
        )
    except (OSError, json.JSONDecodeError, AtlasValidationError) as error:
        raise DomainError(
            code="INPUT_INVALID",
            message="Selected method evidence is not available from the local Method Manifest.",
        ) from error

    expected_manifest_version = f"method-manifest@{manifest.source.commit}"
    if (
        manifest.id != selection.method_id
        or selection.method_manifest_version != expected_manifest_version
        or selection.evidence_revision != manifest.source.commit
        or selection.runtime_status != manifest.runtime_status
        or not set(selection.content_modes).issubset(set(manifest.content_modes))
    ):
        raise DomainError(
            code="INPUT_INVALID",
            message="Selected method evidence does not match the local Method Manifest.",
            action="Return to the Method Atlas and select the current manifest-backed method.",
        )


def _sse_events(events: tuple[JobEvent, ...]) -> Iterator[str]:
    """Serialize durable events using the minimal SSE framing required for reconnect replay."""
    for event in events:
        payload = json.dumps(
            event.model_dump(mode="json"), ensure_ascii=False, separators=(",", ":")
        )
        yield f"id: {event.id}\nevent: progress\ndata: {payload}\n\n"


app = create_app()
