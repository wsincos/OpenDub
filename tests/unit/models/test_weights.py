from pathlib import Path

import httpx
import pytest

from opendub.domain.errors import DomainError
from opendub.models.weights import WeightArtifact, WeightManager


def test_weight_manager_requires_explicit_license_acceptance(tmp_path: Path) -> None:
    artifact = WeightArtifact(
        model_id="example/model",
        role="acoustic_model",
        url="https://weights.example/model.bin",
        sha256="a" * 64,
        license="research-only",
    )

    with pytest.raises(DomainError, match="MODEL_LICENSE_NOT_ACCEPTED"):
        WeightManager(tmp_path).ensure(artifact, license_accepted=False)


def test_weight_manager_verifies_checksum_before_publishing(tmp_path: Path) -> None:
    payload = b"verified model bytes"
    digest = "03cfa25d83f5eaa1faac98ed6ceaaf0e7afe3c273a1e1502c2714ebe10b8263e"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("range") is None
        return httpx.Response(200, content=payload)

    artifact = WeightArtifact(
        model_id="example/model",
        role="acoustic_model",
        url="https://weights.example/model.bin",
        sha256=digest,
        license="Apache-2.0",
    )
    manager = WeightManager(tmp_path, client=httpx.Client(transport=httpx.MockTransport(handler)))

    result = manager.ensure(artifact, license_accepted=True)

    assert result.read_bytes() == payload
    assert not result.with_suffix(".partial").exists()
