from pathlib import Path

from opendub.storage.project_store import ProjectStore
from opendub.storage.sqlite_index import SQLiteIndex


def test_index_rebuilds_from_project_files_after_database_loss(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    first = store.create("First authorized demo")
    second = store.create("Second authorized demo")
    index = SQLiteIndex(tmp_path / "index.sqlite3")

    indexed = index.rebuild(store)
    (tmp_path / "index.sqlite3").unlink()

    rebuilt = SQLiteIndex(tmp_path / "index.sqlite3")
    restored = rebuilt.rebuild(store)

    assert indexed == 2
    assert restored == 2
    assert {project.id for project in rebuilt.list_projects()} == {first.id, second.id}
