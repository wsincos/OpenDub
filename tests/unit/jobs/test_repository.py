from pathlib import Path

from opendub.jobs.repository import JobRepository


def test_events_are_persistent_and_monotonic(tmp_path: Path) -> None:
    repository = JobRepository(tmp_path / "jobs.json")
    job = repository.create(
        project_id="0198baf0-0000-7000-8000-000000000000",
        kind="segment.generate",
    )
    first = repository.append_event(job.id, stage="queue", message="Queued", progress=None)
    second = repository.append_event(job.id, stage="model", message="Generating", progress=0.5)

    restored = JobRepository(tmp_path / "jobs.json")

    assert (first.id, second.id) == (1, 2)
    assert restored.events(job.id, after_id=1) == (second,)


def test_repository_marks_inflight_jobs_interrupted_after_restart(tmp_path: Path) -> None:
    path = tmp_path / "jobs.json"
    repository = JobRepository(path)
    job = repository.create(
        project_id="0198baf0-0000-7000-8000-000000000000",
        kind="segment.generate",
    )
    repository.transition(job.id, "running")

    restored = JobRepository(path)

    assert restored.get(job.id).status == "interrupted"
