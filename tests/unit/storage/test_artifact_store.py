from pathlib import Path

import pytest

from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


def test_artifact_store_uses_content_hash_and_project_relative_path(tmp_path: Path) -> None:
    project = ProjectStore(tmp_path).create("Authorized demo")
    store = ArtifactStore(tmp_path)

    first = store.ingest_bytes(
        project.id,
        kind="audio",
        display_name="Reference.wav",
        data=b"authorized reference audio",
        extension="wav",
    )
    second = store.ingest_bytes(
        project.id,
        kind="audio",
        display_name="Reference copy.wav",
        data=b"authorized reference audio",
        extension="wav",
    )

    assert first.sha256 == second.sha256
    assert first.relative_path == second.relative_path
    assert first.relative_path.startswith("assets/")
    assert (tmp_path / "projects" / project.id / first.relative_path).is_file()


@pytest.mark.parametrize("extension", ["../wav", "wav/evil", "wav.exe"])
def test_artifact_store_rejects_unsafe_extensions(tmp_path: Path, extension: str) -> None:
    project = ProjectStore(tmp_path).create("Authorized demo")

    with pytest.raises(ValueError, match="extension"):
        ArtifactStore(tmp_path).ingest_bytes(
            project.id,
            kind="audio",
            display_name="Reference",
            data=b"audio",
            extension=extension,
        )
