from pathlib import Path

from fastapi.testclient import TestClient

from opendub.api.app import create_app


def test_projects_api_creates_and_reads_local_project(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))

    created = client.post("/api/v1/projects", json={"name": "Authorized demo"})
    project_id = created.json()["id"]
    loaded = client.get(f"/api/v1/projects/{project_id}")

    assert created.status_code == 201
    assert loaded.status_code == 200
    assert loaded.json()["name"] == "Authorized demo"


def test_health_endpoint_declares_local_only_service(tmp_path: Path) -> None:
    response = TestClient(create_app(workspace=tmp_path)).get("/api/v1/health")

    assert response.json() == {"status": "ok", "mode": "local"}


def test_api_allows_only_local_web_studio_origins(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    response = client.options(
        "/api/v1/projects",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
