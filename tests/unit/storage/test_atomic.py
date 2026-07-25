from pathlib import Path

import pytest

from opendub.storage.atomic import atomic_write_text


def test_failed_atomic_replace_preserves_existing_file(tmp_path: Path) -> None:
    target = tmp_path / "project.json"
    target.write_text('{"revision": 1}', encoding="utf-8")

    def fail_replace(_: Path, __: Path) -> None:
        raise OSError("interrupted before replacement")

    with pytest.raises(OSError, match="interrupted"):
        atomic_write_text(target, '{"revision": 2}', replace=fail_replace)

    assert target.read_text(encoding="utf-8") == '{"revision": 1}'
    assert not list(tmp_path.glob("*.partial"))
