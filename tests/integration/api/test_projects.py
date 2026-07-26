from pathlib import Path

import pytest
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


def test_projects_api_persists_a_complete_method_selection(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    created = client.post("/api/v1/projects", json={"name": "Emotion-directed scene"})
    project_id = created.json()["id"]

    selected = client.put(
        f"/api/v1/projects/{project_id}/method-selection",
        json={
            "method_id": "galaxycong/emodubber",
            "method_manifest_version": "method-manifest@553fa054160fed17e757125d185e5a61ef6ed437",
            "declared_need": "Explicit emotion category and intensity control.",
            "required_inputs": ["Video", "Target text", "Authorized reference speech"],
            "optional_controls": ["Emotion category", "Emotion intensity"],
            "runtime_status": "unavailable",
            "content_modes": ["concept"],
            "evidence_revision": "553fa054160fed17e757125d185e5a61ef6ed437",
            "expected_revision": created.json()["revision"],
        },
    )
    loaded = client.get(f"/api/v1/projects/{project_id}")

    assert selected.status_code == 200
    assert selected.json()["method_selection"]["method_id"] == "galaxycong/emodubber"
    assert loaded.json()["method_selection"]["optional_controls"] == [
        "Emotion category",
        "Emotion intensity",
    ]


def test_projects_api_rejects_a_method_selection_with_stale_manifest_evidence(
    tmp_path: Path,
) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    created = client.post("/api/v1/projects", json={"name": "Stale evidence"})

    selected = client.put(
        f"/api/v1/projects/{created.json()['id']}/method-selection",
        json={
            "method_id": "galaxycong/hpmdubbing",
            "method_manifest_version": "method-manifest@not-the-local-commit",
            "declared_need": "Inspect visual prosody.",
            "required_inputs": ["Video", "Target text", "Authorized reference speech"],
            "optional_controls": [],
            "runtime_status": "unavailable",
            "content_modes": ["concept"],
            "evidence_revision": "0000000000000000000000000000000000000000",
            "expected_revision": created.json()["revision"],
        },
    )

    assert selected.status_code == 422
    assert selected.json()["detail"]["code"] == "INPUT_INVALID"
    assert "evidence" in selected.json()["detail"]["message"].lower()


@pytest.mark.parametrize(
    ("method_id", "commit"),
    [
        ("galaxycong/hpmdubbing", "f50dfa7df649208c674f151e52ad0a38d0b0bd43"),
        ("galaxycong/styledubber", "bc431c8f67e885433c5c23163a8eaccb0dd41175"),
        ("galaxycong/emodubber", "553fa054160fed17e757125d185e5a61ef6ed437"),
    ],
)
def test_projects_api_selects_each_core_manifest_backed_method(
    tmp_path: Path, method_id: str, commit: str
) -> None:
    client = TestClient(create_app(workspace=tmp_path))
    created = client.post("/api/v1/projects", json={"name": method_id})

    selected = client.put(
        f"/api/v1/projects/{created.json()['id']}/method-selection",
        json={
            "method_id": method_id,
            "method_manifest_version": f"method-manifest@{commit}",
            "declared_need": "Inspect one complete method.",
            "required_inputs": ["Video", "Target text", "Authorized reference speech"],
            "optional_controls": [],
            "runtime_status": "unavailable",
            "content_modes": ["concept"],
            "evidence_revision": commit,
            "expected_revision": created.json()["revision"],
        },
    )

    assert selected.status_code == 200
    assert selected.json()["method_selection"]["method_id"] == method_id


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

    alternate_port = client.options(
        "/api/v1/projects",
        headers={
            "Origin": "http://127.0.0.1:5174",
            "Access-Control-Request-Method": "POST",
        },
    )
    remote = client.options(
        "/api/v1/projects",
        headers={
            "Origin": "https://example.invalid",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert alternate_port.headers["access-control-allow-origin"] == "http://127.0.0.1:5174"
    assert "access-control-allow-origin" not in remote.headers


def test_api_allows_the_local_studio_when_vite_uses_an_alternate_port(tmp_path: Path) -> None:
    client = TestClient(create_app(workspace=tmp_path))

    response = client.options(
        "/api/v1/projects",
        headers={
            "Origin": "http://127.0.0.1:5180",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5180"


def test_models_endpoint_returns_audited_registry_records(tmp_path: Path) -> None:
    response = TestClient(create_app(workspace=tmp_path)).get("/api/v1/models")

    assert response.status_code == 200
    records = response.json()
    assert any(record["id"] == "galaxycong/emodubber" for record in records)
    assert all(record["maturity"] == "planned" for record in records)
