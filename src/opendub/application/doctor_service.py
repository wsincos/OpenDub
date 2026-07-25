"""Privacy-preserving local environment diagnostics for OpenDub workflows."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from opendub.models.audit import validate_upstream_registry

CheckStatus = Literal["ok", "failed"]
CommandRunner = Callable[[tuple[str, ...]], bool]


class DoctorCheck(BaseModel):
    """One concise diagnostic result safe to display or serialize."""

    model_config = ConfigDict(frozen=True)

    id: str
    status: CheckStatus
    message: str


class DoctorReport(BaseModel):
    """Aggregate of local checks without local content, paths, or credentials."""

    model_config = ConfigDict(frozen=True)

    ready: bool
    checks: tuple[DoctorCheck, ...]


def run_doctor(
    *,
    workspace: Path,
    registry_path: Path,
    run_command: CommandRunner | None = None,
) -> DoctorReport:
    """Check only prerequisites required for a private local OpenDub workspace."""
    command = run_command or _run_command
    checks = (
        _check_workspace(workspace),
        _check_ffmpeg(command),
        _check_registry(registry_path),
    )
    return DoctorReport(ready=all(check.status == "ok" for check in checks), checks=checks)


def _check_workspace(workspace: Path) -> DoctorCheck:
    try:
        workspace.mkdir(parents=True, exist_ok=True)
        probe = workspace / ".opendub-write-probe"
        probe.write_text("ok", encoding="ascii")
        probe.unlink()
    except OSError:
        return DoctorCheck(
            id="workspace.writable",
            status="failed",
            message="The local workspace is not writable.",
        )
    return DoctorCheck(
        id="workspace.writable",
        status="ok",
        message="Local workspace is writable.",
    )


def _check_ffmpeg(run_command: CommandRunner) -> DoctorCheck:
    if run_command(("ffmpeg", "-version")):
        return DoctorCheck(id="ffmpeg", status="ok", message="FFmpeg is available.")
    return DoctorCheck(id="ffmpeg", status="failed", message="FFmpeg is not available on PATH.")


def _check_registry(registry_path: Path) -> DoctorCheck:
    if not registry_path.is_file():
        return DoctorCheck(id="registry", status="failed", message="Model registry is missing.")
    result = validate_upstream_registry(registry_path)
    if result.is_valid:
        return DoctorCheck(id="registry", status="ok", message="Model registry is valid.")
    return DoctorCheck(
        id="registry",
        status="failed",
        message="Model registry has invalid entries.",
    )


def _run_command(command: tuple[str, ...]) -> bool:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return False
    return completed.returncode == 0
