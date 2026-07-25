"""Evaluate persisted candidate audio without claiming unavailable neural metrics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]

from opendub.domain.assets import MediaAsset
from opendub.domain.errors import DomainError
from opendub.domain.metrics import MetricResult
from opendub.evaluation.audio_quality import clipping_ratio, integrated_lufs, silence_ratio
from opendub.evaluation.report import CandidateEvaluationReport, render_markdown, serialize_report
from opendub.evaluation.sync import duration_error
from opendub.storage.atomic import atomic_write_text
from opendub.storage.project_store import ProjectStore


class EvaluationService:
    """Persist deterministic audio checks plus explicit unavailable advanced-metric records."""

    def __init__(self, store: ProjectStore) -> None:
        self.store = store

    def evaluate_candidate(self, project_id: str, candidate_id: str) -> CandidateEvaluationReport:
        """Evaluate a stored candidate at its recorded segment revision."""
        project = self.store.load(project_id)
        candidate = next((item for item in project.candidates if item.id == candidate_id), None)
        if candidate is None:
            raise DomainError(code="ASSET_NOT_FOUND", message="Generated candidate was not found.")
        segment = next((item for item in project.segments if item.id == candidate.segment_id), None)
        audio = next((item for item in project.assets if item.id == candidate.audio_asset_id), None)
        if segment is None or audio is None or audio.kind != "audio":
            raise DomainError(
                code="ASSET_NOT_FOUND", message="Candidate input data was not found in the project."
            )
        samples, sample_rate = sf.read(
            self._asset_path(project.id, audio), dtype="float32", always_2d=True
        )
        mono = np.mean(np.asarray(samples, dtype=np.float32), axis=1)
        metrics = (
            duration_error(
                target_duration_us=segment.range.duration_us,
                duration_samples=len(mono),
                sample_rate=sample_rate,
            ),
            silence_ratio(mono),
            clipping_ratio(mono),
            integrated_lufs(mono, sample_rate=sample_rate),
            _unavailable("content.transcript_match", "No pinned ASR metric model is installed."),
            _unavailable("speaker.similarity", "No pinned speaker metric model is installed."),
            _unavailable("emotion.direction", "No pinned emotion metric model is installed."),
        )
        report_dir = (
            self.store.project_dir(project.id) / "reports" / candidate.id / f"r{candidate.revision}"
        )
        report = CandidateEvaluationReport(
            candidate_id=candidate.id,
            project_id=project.id,
            json_path=report_dir / "evaluation.json",
            markdown_path=report_dir / "evaluation.md",
            metrics=metrics,
        )
        atomic_write_text(
            report.json_path,
            serialize_report(
                report,
                segment_id=segment.id,
                segment_revision=candidate.segment_revision,
                target_duration_us=segment.range.duration_us,
                audio_sha256=audio.sha256,
            ),
        )
        atomic_write_text(report.markdown_path, render_markdown(report))
        return report

    def _asset_path(self, project_id: str, asset: MediaAsset) -> Path:
        project_dir = self.store.project_dir(project_id)
        asset_root = (project_dir / "assets").resolve()
        path = (project_dir / asset.relative_path).resolve()
        if not path.is_relative_to(asset_root) or not path.is_file():
            raise DomainError(code="ASSET_NOT_FOUND", message="Candidate audio data was not found.")
        return path


def _unavailable(metric_id: str, reason: str) -> MetricResult:
    return MetricResult(
        metric_id=metric_id,
        version="not-installed",
        status="unavailable",
        details={"reason": reason},
    )
