"""A disposable SQLite search index rebuilt entirely from project manifests."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from opendub.storage.project_store import ProjectStore


@dataclass(frozen=True)
class IndexedProject:
    """A small project projection for list and search views."""

    id: str
    name: str
    revision: int
    updated_at: str


class SQLiteIndex:
    """Maintain a non-authoritative project index with explicit rebuild support."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def rebuild(self, store: ProjectStore) -> int:
        """Discard derived rows and rebuild them solely from ``project.json`` files."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            self._initialize(connection)
            connection.execute("DELETE FROM project_index")
            projects = store.iter_projects()
            connection.executemany(
                """
                INSERT INTO project_index (id, name, revision, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (project.id, project.name, project.revision, project.updated_at.isoformat())
                    for project in projects
                ],
            )
        return len(projects)

    def list_projects(self) -> tuple[IndexedProject, ...]:
        """List index records ordered by most recently modified project first."""
        if not self.path.is_file():
            return ()
        with sqlite3.connect(self.path) as connection:
            self._initialize(connection)
            rows = connection.execute(
                """
                SELECT id, name, revision, updated_at
                FROM project_index
                ORDER BY updated_at DESC, id DESC
                """
            ).fetchall()
        return tuple(IndexedProject(*row) for row in rows)

    @staticmethod
    def _initialize(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS project_index (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                revision INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
