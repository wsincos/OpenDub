"""Durable same-directory atomic writes for local project manifests."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from uuid import uuid4

ReplaceOperation = Callable[[Path, Path], None]


def atomic_write_text(
    path: Path,
    content: str,
    *,
    replace: ReplaceOperation = os.replace,
) -> None:
    """Atomically replace a UTF-8 file after syncing the temporary file to disk."""
    atomic_write_bytes(path, content.encode("utf-8"), replace=replace)


def atomic_write_bytes(
    path: Path,
    content: bytes,
    *,
    replace: ReplaceOperation = os.replace,
) -> None:
    """Atomically replace a file without exposing a partially written destination."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.partial")
    try:
        with temporary.open("xb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _sync_directory(directory: Path) -> None:
    """Persist the rename metadata when the operating system supports it."""
    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
