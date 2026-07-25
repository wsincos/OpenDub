"""Portable candidate evaluation report structures and deterministic serializers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from opendub.domain.metrics import MetricResult


@dataclass(frozen=True)
class CandidateEvaluationReport:
    """Stable locations and metric values emitted for one candidate evaluation."""

    candidate_id: str
    project_id: str
    json_path: Path
    markdown_path: Path
    metrics: tuple[MetricResult, ...]


def serialize_report(
    report: CandidateEvaluationReport,
    *,
    segment_id: str,
    segment_revision: int,
    target_duration_us: int,
    audio_sha256: str,
) -> str:
    """Return a portable report JSON document with no local absolute paths."""
    return (
        json.dumps(
            {
                "schema_version": "opendub.evaluation-report/v1",
                "project_id": report.project_id,
                "candidate_id": report.candidate_id,
                "segment_id": segment_id,
                "segment_revision": segment_revision,
                "target_duration_us": target_duration_us,
                "input_hashes": {"candidate_audio": audio_sha256},
                "metrics": [metric.model_dump(mode="json") for metric in report.metrics],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def render_markdown(report: CandidateEvaluationReport) -> str:
    """Render an intentionally compact human summary without exposing source-media paths."""
    rows = ["| Metric | Status | Value | Unit |", "| --- | --- | ---: | --- |"]
    for metric in report.metrics:
        value = "-" if metric.value is None else f"{metric.value:.6g}"
        rows.append(f"| `{metric.metric_id}` | {metric.status} | {value} | {metric.unit or '-'} |")
    unavailable = [metric.metric_id for metric in report.metrics if metric.status != "ok"]
    limitations = (
        "All reported metrics were computed."
        if not unavailable
        else "Unavailable or inapplicable metrics: "
        + ", ".join(f"`{metric}`" for metric in unavailable)
        + "."
    )
    return "\n".join(
        [
            "# Candidate Evaluation",
            "",
            f"Candidate: `{report.candidate_id}`",
            "",
            *rows,
            "",
            "## Limitations",
            "",
            limitations,
            "",
        ]
    )
