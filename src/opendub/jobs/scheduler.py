"""A deterministic single-host scheduler with serialized GPU execution."""

from __future__ import annotations

from collections.abc import Callable

from opendub.domain.errors import DomainError
from opendub.jobs.models import JobRecord, JobResource, JobStatus
from opendub.jobs.repository import JobRepository
from opendub.pipeline.cancellation import CancellationToken

Operation = Callable[["JobContext"], object]


class JobContext:
    """A narrow task callback interface for events and cooperative cancellation."""

    def __init__(
        self,
        repository: JobRepository,
        job: JobRecord,
        cancellation: CancellationToken,
    ) -> None:
        self.repository = repository
        self.job = job
        self.cancellation = cancellation

    def progress(self, stage: str, message: str, progress: float | None) -> None:
        """Persist a structured progress event, unless cancellation was requested."""
        if self.cancellation.cancelled:
            raise DomainError(code="JOB_CANCELLED", message="Job was cancelled.")
        self.repository.append_event(self.job.id, stage=stage, message=message, progress=progress)


class JobScheduler:
    """Run queued work deterministically; one call to ``run_next`` executes one job."""

    def __init__(self, repository: JobRepository) -> None:
        self.repository = repository
        self._operations: dict[str, Operation] = {}
        self._cancellations: dict[str, CancellationToken] = {}

    def enqueue(
        self,
        *,
        project_id: str,
        kind: str,
        resource: JobResource,
        operation: Operation,
    ) -> JobRecord:
        """Persist a job and retain its in-process operation until it is run."""
        if resource not in {"cpu", "gpu"}:
            raise ValueError("resource must be cpu or gpu")
        job = self.repository.create(project_id=project_id, kind=kind, resource=resource)
        self._operations[job.id] = operation
        self._cancellations[job.id] = CancellationToken()
        self.repository.append_event(job.id, stage="queue", message="Queued", progress=None)
        return job

    def cancel(self, job_id: str) -> None:
        """Cancel queued work immediately or signal an in-flight operation cooperatively."""
        job = self.repository.get(job_id)
        if job.status == "queued":
            self.repository.transition(job_id, "cancelled")
            self.repository.append_event(job_id, stage="queue", message="Cancelled", progress=None)
            return
        if job.status == "running":
            self.repository.transition(job_id, "cancelling")
            self._cancellations[job_id].cancel()

    def run_next(self) -> JobRecord | None:
        """Execute exactly one queued job, naturally serializing all GPU work."""
        queued = self.repository.queued()
        if not queued:
            return None
        job = queued[0]
        operation = self._operations.get(job.id)
        if operation is None:
            self.repository.transition(job.id, "interrupted")
            return self.repository.get(job.id)
        self.repository.transition(job.id, "running")
        context = JobContext(self.repository, job, self._cancellations[job.id])
        try:
            operation(context)
        except DomainError as error:
            target: JobStatus = "cancelled" if error.code == "JOB_CANCELLED" else "failed"
            self.repository.transition(job.id, target)
            self.repository.append_event(
                job.id,
                stage="scheduler",
                message=error.message,
                progress=None,
            )
        except Exception as error:
            self.repository.transition(job.id, "failed")
            self.repository.append_event(
                job.id,
                stage="scheduler",
                message="Job failed.",
                progress=None,
                level="error",
            )
            raise error
        else:
            self.repository.transition(job.id, "succeeded")
            self.repository.append_event(
                job.id,
                stage="scheduler",
                message="Succeeded",
                progress=1.0,
            )
        return self.repository.get(job.id)
