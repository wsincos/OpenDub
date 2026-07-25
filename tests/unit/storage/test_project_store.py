from pathlib import Path

import pytest

from opendub.domain.errors import DomainError
from opendub.storage.project_store import ProjectStore


def test_store_creates_and_loads_file_backed_project(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)

    created = store.create("Authorized demo")
    loaded = store.load(created.id)

    assert loaded == created
    assert (tmp_path / "projects" / created.id / "project.json").is_file()


def test_store_rejects_stale_save_revision(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    created = store.create("Authorized demo")
    revised = created.model_copy(update={"name": "Revised demo", "revision": 2})
    store.save(revised, expected_revision=1)

    with pytest.raises(DomainError, match="PROJECT_CONFLICT"):
        store.save(revised, expected_revision=1)
