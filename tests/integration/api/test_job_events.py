import json
from pathlib import Path

from fastapi.testclient import TestClient

from opendub.api.app import create_app
from opendub.jobs.repository import JobRepository
from opendub.storage.project_store import ProjectStore


def test_api_lists_persisted_project_jobs_and_replays_sse_events(tmp_path: Path) -> None:
    project = ProjectStore(tmp_path).create("Observable jobs")
    jobs = JobRepository(tmp_path / "jobs.json")
    job = jobs.create(project_id=project.id, kind="generation", resource="gpu")
    event = jobs.append_event(job.id, stage="queue", message="Queued", progress=None)
    client = TestClient(create_app(workspace=tmp_path))

    listed = client.get(f"/api/v1/projects/{project.id}/jobs")
    replay = client.get(f"/api/v1/jobs/{job.id}/events?after_id=0")
    exhausted = client.get(f"/api/v1/jobs/{job.id}/events?after_id={event.id}")

    assert listed.status_code == 200
    assert listed.json()[0]["id"] == job.id
    assert replay.status_code == 200
    assert replay.headers["content-type"].startswith("text/event-stream")
    assert f"id: {event.id}" in replay.text
    assert json.dumps("Queued") in replay.text
    assert exhausted.status_code == 200
    assert exhausted.text == ""
