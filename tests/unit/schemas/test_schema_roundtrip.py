from datetime import UTC, datetime
from pathlib import Path

import jsonschema
import pytest

from opendub.domain.project import Project
from opendub.schemas.export import export_schemas
from opendub.schemas.models import RunManifest


def test_exported_project_schema_validates_the_same_project_as_pydantic(tmp_path: Path) -> None:
    written = export_schemas(tmp_path)
    project = Project(name="Authorized demo")

    jsonschema.validate(project.model_dump(mode="json"), written["project-v1.json"])


def test_exported_project_schema_rejects_invalid_revision(tmp_path: Path) -> None:
    written = export_schemas(tmp_path)
    payload = Project(name="Authorized demo").model_dump(mode="json")
    payload["revision"] = 0

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, written["project-v1.json"])


def test_run_manifest_is_versioned_and_serializable() -> None:
    manifest = RunManifest(
        id="run-001",
        project_id="019f9964-25bd-75b5-8f36-da5a6d0322d6",
        segment_id="019f9964-25bd-75b5-8f36-da5a6d0322d6",
        adapter_id="opendub.test",
        adapter_version="0.1.0",
        model_id="opendub/test",
        weights_sha256="a" * 64,
        seed=7,
        created_at=datetime.now(UTC),
    )

    assert manifest.schema_version == "opendub.run/v1"
    assert manifest.model_dump(mode="json")["weights_sha256"] == "a" * 64
