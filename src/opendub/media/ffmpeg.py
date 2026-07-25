"""A shell-free FFmpeg subprocess boundary."""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class FfmpegResult:
    """Captured result from one deterministic FFmpeg invocation."""

    command: tuple[str, ...]
    stdout: str
    stderr: str


class FfmpegError(RuntimeError):
    """Raised when FFmpeg exits unsuccessfully, with a bounded diagnostic."""


class CommandRunner(Protocol):
    """Minimal boundary used by deterministic media helpers and their tests."""

    def run(self, arguments: Sequence[str]) -> FfmpegResult: ...


class FfmpegRunner:
    """Execute FFmpeg with argument arrays only; never invoke a shell."""

    def __init__(self, executable: str = "ffmpeg") -> None:
        self.executable = executable

    def run(self, arguments: Sequence[str]) -> FfmpegResult:
        """Run FFmpeg and return captured output or raise ``FfmpegError``."""
        command = [self.executable, *arguments]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
        result = FfmpegResult(tuple(command), completed.stdout, completed.stderr)
        if completed.returncode != 0:
            message = completed.stderr[-4_000:] or "FFmpeg failed without stderr output."
            raise FfmpegError(message)
        return result


def ensure_parent(path: Path) -> None:
    """Create an output directory without interpreting it as executable input."""
    path.parent.mkdir(parents=True, exist_ok=True)
