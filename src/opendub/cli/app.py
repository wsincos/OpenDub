"""Typer commands for local-first project creation and inspection."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
import uvicorn

from opendub.application.doctor_service import run_doctor
from opendub.storage.project_store import ProjectStore

app = typer.Typer(add_completion=False, help="OpenDub local video dubbing workspace.")


@app.command()
def init(
    workspace: Annotated[
        Path,
        typer.Option(help="Local OpenDub workspace directory."),
    ] = Path(".opendub"),
) -> None:
    """Initialize an empty private local workspace."""
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "projects").mkdir(exist_ok=True)
    typer.echo("Initialized local OpenDub workspace.")


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


@app.command()
def doctor(
    workspace: Annotated[
        Path,
        typer.Option(help="Local OpenDub workspace directory."),
    ] = Path(".opendub"),
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON without terminal styling."),
    ] = False,
) -> None:
    """Check the local workspace, FFmpeg, and upstream registry evidence."""
    repository_root = Path(__file__).resolve().parents[3]
    report = run_doctor(
        workspace=workspace,
        registry_path=repository_root / "model-registry" / "upstreams.yaml",
    )
    if json_output:
        typer.echo(report.model_dump_json())
    else:
        for check in report.checks:
            typer.echo(f"{check.status.upper()}\t{check.id}\t{check.message}")
    if not report.ready:
        raise typer.Exit(code=1)


@app.command()
def serve(
    workspace: Annotated[
        Path,
        typer.Option(help="Local OpenDub workspace directory."),
    ] = Path(".opendub"),
    host: Annotated[
        str,
        typer.Option(help="Bind address. Use the local default unless remote access is intended."),
    ] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Local HTTP port.")] = 8000,
) -> None:
    """Serve the local API for OpenDub Studio."""
    from opendub.api.app import create_app

    uvicorn.run(create_app(workspace=workspace), host=host, port=port)
