"""Content-addressed project artifacts that cannot escape their project root."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from opendub.domain.assets import AssetKind, MediaAsset
from opendub.storage.atomic import atomic_write_bytes
from opendub.storage.project_store import ProjectStore

_EXTENSION_PATTERN = re.compile(r"^[a-z0-9]{1,10}$")


class ArtifactStore:
    """Persist generated or ingested bytes underneath one project's assets directory."""

    def __init__(self, root: Path) -> None:
        self.project_store = ProjectStore(root)

    def ingest_bytes(
        self,
        project_id: str,
        *,
        kind: AssetKind,
        display_name: str,
        data: bytes,
        extension: str,
    ) -> MediaAsset:
        """Store bytes under their SHA-256 and return portable asset metadata."""
        if not _EXTENSION_PATTERN.fullmatch(extension):
            raise ValueError("extension must contain 1-10 lowercase alphanumeric characters")
        digest = hashlib.sha256(data).hexdigest()
        relative_path = f"assets/{digest}.{extension}"
        destination = self.project_store.project_dir(project_id) / relative_path
        if not destination.is_file():
            atomic_write_bytes(destination, data)
        return MediaAsset(
            kind=kind,
            display_name=display_name,
            relative_path=relative_path,
            sha256=digest,
            size_bytes=len(data),
        )
