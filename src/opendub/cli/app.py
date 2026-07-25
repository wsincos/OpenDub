"""Typer commands for local-first project creation and inspection."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from opendub.storage.project_store import ProjectStore

app = typer.Typer(add_completion=False, help="OpenDub local video dubbing workspace.")


@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Project display name.")],
    workspace: Annotated[
        Path,
        typer.Option(help="Local OpenDub workspace directory."),
    ] = Path(".opendub"),
) -> None:
    """Create a file-backed local project."""
    project = ProjectStore(workspace).create(name)
    typer.echo(f"Created {project.name} ({project.id})")


@app.command("list")
def list_projects(
    workspace: Annotated[
        Path,
        typer.Option(help="Local OpenDub workspace directory."),
    ] = Path(".opendub"),
) -> None:
    """List projects in a local workspace."""
    for project in ProjectStore(workspace).iter_projects():
        typer.echo(f"{project.id}\t{project.name}\trevision={project.revision}")
