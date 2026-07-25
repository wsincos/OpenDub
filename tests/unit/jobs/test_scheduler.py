from pathlib import Path

from opendub.jobs.repository import JobRepository
from opendub.jobs.scheduler import JobScheduler


def test_scheduler_runs_gpu_jobs_serially_and_reports_progress(tmp_path: Path) -> None:
    repository = JobRepository(tmp_path / "jobs.json")
    scheduler = JobScheduler(repository)
    calls: list[str] = []

    first = scheduler.enqueue(
        project_id="0198baf0-0000-7000-8000-000000000000",
        kind="segment.generate",
        resource="gpu",
        operation=lambda context: (calls.append("first"), context.progress("model", "Done", 1.0)),
    )
    second = scheduler.enqueue(
        project_id="0198baf0-0000-7000-8000-000000000000",
        kind="segment.generate",
        resource="gpu",
        operation=lambda context: calls.append("second"),
    )

    scheduler.run_next()
    scheduler.run_next()

    assert calls == ["first", "second"]
    assert repository.get(first.id).status == "succeeded"
    assert repository.get(second.id).status == "succeeded"
    assert repository.events(first.id, after_id=0)[-1].progress == 1.0
