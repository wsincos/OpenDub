"""Local-only HTTP application backed directly by the file project store."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from opendub.domain.errors import DomainError
from opendub.domain.project import Project
from opendub.storage.project_store import ProjectStore


class CreateProjectRequest(BaseModel):
    """Validated request body for creating a new local project."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)


def create_app(*, workspace: Path | None = None) -> FastAPI:
    """Create an API application that defaults to a private local workspace."""
    root = (workspace or Path.cwd() / ".opendub").resolve()
    store = ProjectStore(root)
    app = FastAPI(title="OpenDub Local API", version="0.0.1a0", docs_url="/api/docs")

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "local"}

    @app.post("/api/v1/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
    def create_project(request: CreateProjectRequest) -> Project:
        return store.create(request.name)

    @app.get("/api/v1/projects/{project_id}", response_model=Project)
    def get_project(project_id: str) -> Project:
        try:
            return store.load(project_id)
        except DomainError as error:
            raise _http_error(error) from error

    @app.get("/api/v1/projects", response_model=tuple[Project, ...])
    def list_projects() -> tuple[Project, ...]:
        return store.iter_projects()

    return app


def _http_error(error: DomainError) -> HTTPException:
    status_code = (
        status.HTTP_409_CONFLICT if error.code == "PROJECT_CONFLICT" else status.HTTP_404_NOT_FOUND
    )
    return HTTPException(
        status_code=status_code,
        detail={"code": error.code, "message": error.message, "action": error.action},
    )


app = create_app()
