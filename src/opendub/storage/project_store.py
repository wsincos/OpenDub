"""The file-backed source of truth for OpenDub projects."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from pydantic import ValidationError

from opendub.domain.errors import DomainError
from opendub.domain.ids import validate_uuid7
from opendub.domain.project import Project
from opendub.storage.atomic import atomic_write_text


class ProjectStore:
    """Create and update versioned projects rooted in a single local workspace."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.projects_dir = self.root / "projects"

    def create(self, name: str) -> Project:
        """Create a new project and persist its first manifest atomically."""
        project = Project(name=name)
        self._write_project(project)
        return project

    def load(self, project_id: str) -> Project:
        """Load and validate a project manifest by its UUIDv7 identifier."""
        manifest = self.project_dir(project_id) / "project.json"
        if not manifest.is_file():
            raise DomainError(code="ASSET_NOT_FOUND", message="Project manifest was not found.")
        try:
            return Project.model_validate_json(manifest.read_text(encoding="utf-8"))
        except (OSError, ValidationError) as error:
            raise DomainError(
                code="INPUT_INVALID",
                message="Project manifest is unreadable or invalid.",
            ) from error

    def save(self, project: Project, expected_revision: int) -> Project:
        """Persist the next revision, rejecting stale or skipped updates."""
        persisted = self.load(project.id)
        if persisted.revision != expected_revision:
            raise DomainError(
                code="PROJECT_CONFLICT",
                message="Project was changed by another operation.",
                action="Reload the project and retry the change.",
            )
        if project.revision != persisted.revision + 1:
            raise DomainError(
                code="INPUT_INVALID",
                message="Saved project revision must increment by exactly one.",
            )
        self._write_project(project)
        return project

    def delete(self, project_id: str) -> None:
        """Delete only a project directory, never shared model or artifact caches."""
        directory = self.project_dir(project_id)
        if not directory.exists():
            raise DomainError(code="ASSET_NOT_FOUND", message="Project directory was not found.")
        shutil.rmtree(directory)

    def project_dir(self, project_id: str) -> Path:
        """Return a project directory after validating its safe, canonical identifier."""
        return self.projects_dir / validate_uuid7(project_id)

    def iter_projects(self) -> tuple[Project, ...]:
        """Read all valid project manifests from the file-backed source of truth."""
        if not self.projects_dir.is_dir():
            return ()
        projects: list[Project] = []
        for manifest in sorted(self.projects_dir.glob("*/project.json")):
            projects.append(Project.model_validate_json(manifest.read_text(encoding="utf-8")))
        return tuple(projects)

    def _write_project(self, project: Project) -> None:
        content = json.dumps(
            project.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        atomic_write_text(self.project_dir(project.id) / "project.json", f"{content}\n")
