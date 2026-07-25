"""Explicit-license, checksum-verified model weight acquisition."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import httpx
from pydantic import BaseModel, ConfigDict, Field

from opendub.domain.errors import DomainError


class WeightArtifact(BaseModel):
    """One immutable downloadable model artifact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    model_id: str = Field(min_length=1)
    role: str = Field(min_length=1)
    url: str = Field(pattern=r"^https://")
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    license: str = Field(min_length=1)
    size_bytes: int | None = Field(default=None, gt=0)


class WeightManager:
    """Download weights into a shared cache without publishing unverified bytes."""

    def __init__(self, cache_dir: Path, *, client: httpx.Client | None = None) -> None:
        self.cache_dir = cache_dir
        self.client = client

    def ensure(self, artifact: WeightArtifact, *, license_accepted: bool) -> Path:
        """Return a verified cached artifact, downloading it only after confirmation."""
        if not license_accepted:
            raise DomainError(
                code="MODEL_LICENSE_NOT_ACCEPTED",
                message=f"License acceptance is required for {artifact.model_id}:{artifact.role}.",
                action="Review and accept the model weight license before downloading.",
            )
        if artifact.license.lower() == "unknown":
            raise DomainError(
                code="MODEL_LICENSE_NOT_ACCEPTED",
                message=f"Weight license is not verified for {artifact.model_id}:{artifact.role}.",
            )

        destination = self.cache_dir / "artifacts" / artifact.sha256
        if destination.is_file() and _sha256(destination) == artifact.sha256:
            return destination
        partial = destination.with_suffix(".partial")
        destination.parent.mkdir(parents=True, exist_ok=True)
        existing_size = partial.stat().st_size if partial.is_file() else 0
        headers = {"Range": f"bytes={existing_size}-"} if existing_size else {}

        with self._client().stream("GET", artifact.url, headers=headers) as response:
            response.raise_for_status()
            append = existing_size > 0 and response.status_code == 206
            with partial.open("ab" if append else "wb") as handle:
                for chunk in response.iter_bytes():
                    handle.write(chunk)
                handle.flush()
                os.fsync(handle.fileno())

        if artifact.size_bytes is not None and partial.stat().st_size != artifact.size_bytes:
            raise DomainError(
                code="MODEL_WEIGHTS_MISSING",
                message="Downloaded weight size does not match.",
            )
        if _sha256(partial) != artifact.sha256:
            raise DomainError(
                code="MODEL_WEIGHTS_MISSING",
                message="Downloaded weight checksum does not match.",
            )
        os.replace(partial, destination)
        return destination

    def _client(self) -> httpx.Client:
        if self.client is None:
            self.client = httpx.Client(timeout=60.0, follow_redirects=True, trust_env=False)
        return self.client


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest()
