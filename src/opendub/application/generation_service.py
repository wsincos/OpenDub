"""Traceable segment generation orchestration independent of upstream model code."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from opendub.domain.candidates import Candidate
from opendub.domain.errors import DomainError
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment
from opendub.models.protocols import AudioArtifact
from opendub.schemas.models import RunManifest
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


class SegmentAudioGenerator(Protocol):
    """A narrow generation contract shared by real adapters and test fixtures."""

    adapter_id: str
    adapter_version: str
    model_id: str
    weights_sha256: str

    def generate(
        self,
        segment: DubbingSegment,
        destination: Path,
        *,
        seed: int,
    ) -> AudioArtifact: ...


class GenerationService:
    """Persist standard candidate artifacts and a reproducible run manifest."""

    def __init__(self, store: ProjectStore, generator: SegmentAudioGenerator) -> None:
        self.store = store
        self.generator = generator
        self.artifacts = ArtifactStore(store.root)

    def generate_segment(
        self,
        project_id: str,
        segment_id: str,
        *,
        expected_revision: int,
        seed: int,
    ) -> Candidate:
        """Generate one candidate without silently accepting stale project state."""
        project = self.store.load(project_id)
        if project.revision != expected_revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed before generation started.",
                action="Reload the project and generate from the current revision.",
            )
        segment = next((item for item in project.segments if item.id == segment_id), None)
        if segment is None:
            raise DomainError(code="ASSET_NOT_FOUND", message="Dubbing segment was not found.")
        if segment.status != "ready":
            raise DomainError(
                code="INPUT_INVALID",
                message="Segment must be ready before generating a candidate.",
            )
        if segment.adapter_id != self.generator.adapter_id:
            raise DomainError(
                code="MODEL_CAPABILITY_MISMATCH",
                message="Selected generator does not match the segment adapter.",
            )

        candidate_id = new_id()
        candidate_dir = (
            self.store.project_dir(project.id)
            / "segments"
            / segment.id
            / "candidates"
            / candidate_id
        )
        audio = self.generator.generate(segment, candidate_dir / "audio.wav", seed=seed)
        audio_asset = self.artifacts.ingest_bytes(
            project.id,
            kind="audio",
            display_name=f"Candidate {candidate_id}.wav",
            data=audio.path.read_bytes(),
            extension="wav",
        )
        candidate = Candidate(
            id=candidate_id,
            segment_id=segment.id,
            segment_revision=segment.revision + 1,
            audio_asset_id=audio_asset.id,
            adapter_id=self.generator.adapter_id,
            model_id=self.generator.model_id,
            seed=seed,
        )
        manifest = RunManifest(
            id=candidate.id,
            project_id=project.id,
            segment_id=segment.id,
            adapter_id=self.generator.adapter_id,
            adapter_version=self.generator.adapter_version,
            model_id=self.generator.model_id,
            weights_sha256=self.generator.weights_sha256,
            seed=seed,
            input_hashes={"audio": audio.sha256},
            options={"target_duration_us": segment.range.duration_us},
        )
        (candidate_dir / "run.json").write_text(
            manifest.model_dump_json(indent=2),
            encoding="utf-8",
        )
        updated = project.record_generated_candidate(candidate, audio_asset, expected_revision)
        self.store.save(updated, expected_revision=expected_revision)
        return candidate
