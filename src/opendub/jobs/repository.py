"""An atomically persisted JSON job ledger with restart recovery semantics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from opendub.domain.errors import DomainError
from opendub.jobs.models import JobEvent, JobRecord, JobResource, JobStatus
from opendub.storage.atomic import atomic_write_text

_TERMINAL_STATES = frozenset({"succeeded", "failed", "cancelled", "interrupted"})
_ALLOWED_TRANSITIONS: dict[JobStatus, frozenset[JobStatus]] = {
    "queued": frozenset({"running", "cancelled"}),
    "running": frozenset({"succeeded", "failed", "cancelling", "interrupted"}),
    "cancelling": frozenset({"cancelled", "failed", "interrupted"}),
    "succeeded": frozenset(),
    "failed": frozenset(),
    "cancelled": frozenset(),
    "interrupted": frozenset(),
}


class JobRepository:
    """Store jobs and events in a small local ledger independent of model processes."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._jobs: dict[str, JobRecord] = {}
        self._events: list[JobEvent] = []
        self._next_event_id = 1
        self._load()

    def create(self, *, project_id: str, kind: str, resource: JobResource = "cpu") -> JobRecord:
        """Create a queued job and persist it immediately."""
        job = JobRecord(project_id=project_id, kind=kind, resource=resource)
        self._jobs[job.id] = job
        self._persist()
        return job

    def get(self, job_id: str) -> JobRecord:
        """Return a job or raise a stable missing-resource error."""
        try:
            return self._jobs[job_id]
        except KeyError as error:
            raise DomainError(code="ASSET_NOT_FOUND", message="Job was not found.") from error

    def queued(self) -> tuple[JobRecord, ...]:
        """Return queued jobs in creation order."""
        return tuple(job for job in self._jobs.values() if job.status == "queued")

    def list(self, *, project_id: str | None = None) -> tuple[JobRecord, ...]:
        """Return jobs in creation order, optionally constrained to one local project."""
        return tuple(
            job for job in self._jobs.values() if project_id is None or job.project_id == project_id
        )

    def transition(self, job_id: str, target: JobStatus) -> JobRecord:
        """Move a job through the explicit local scheduler state machine."""
        current = self.get(job_id)
        if target not in _ALLOWED_TRANSITIONS[current.status]:
            raise DomainError(
                code="INPUT_INVALID",
                message=f"Cannot transition job from {current.status} to {target}.",
            )
        revised = current.model_copy(
            update={"status": target, "revision": current.revision + 1},
        )
        self._jobs[job_id] = revised
        self._persist()
        return revised

    def append_event(
        self,
        job_id: str,
        *,
        stage: str,
        message: str,
        progress: float | None,
        level: Literal["info", "warning", "error"] = "info",
    ) -> JobEvent:
        """Append a globally monotonic event after confirming the job exists."""
        self.get(job_id)
        event = JobEvent(
            id=self._next_event_id,
            job_id=job_id,
            stage=stage,
            message=message,
            progress=progress,
            level=level,
        )
        self._next_event_id += 1
        self._events.append(event)
        self._persist()
        return event

    def events(self, job_id: str, *, after_id: int = 0) -> tuple[JobEvent, ...]:
        """Return a reconnect-safe ordered event suffix for one job."""
        return tuple(
            event for event in self._events if event.job_id == job_id and event.id > after_id
        )

    def _load(self) -> None:
        if not self.path.is_file():
            return
        document = json.loads(self.path.read_text(encoding="utf-8"))
        jobs = [JobRecord.model_validate(item) for item in document.get("jobs", [])]
        self._jobs = {job.id: job for job in jobs}
        self._events = [JobEvent.model_validate(item) for item in document.get("events", [])]
        self._next_event_id = int(document.get("next_event_id", len(self._events) + 1))
        recovered = False
        for job_id, job in self._jobs.items():
            if job.status in {"running", "cancelling"}:
                self._jobs[job_id] = job.model_copy(
                    update={"status": "interrupted", "revision": job.revision + 1}
                )
                recovered = True
        if recovered:
            self._persist()

    def _persist(self) -> None:
        document = {
            "jobs": [job.model_dump(mode="json") for job in self._jobs.values()],
            "events": [event.model_dump(mode="json") for event in self._events],
            "next_event_id": self._next_event_id,
        }
        atomic_write_text(self.path, f"{json.dumps(document, sort_keys=True)}\n")
