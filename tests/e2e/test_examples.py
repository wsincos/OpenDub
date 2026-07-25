import subprocess
import sys
from pathlib import Path

from opendub.storage.project_store import ProjectStore


def test_example_builder_creates_two_authorized_local_projects(tmp_path: Path) -> None:
    script = Path(__file__).parents[2] / "scripts" / "build_examples.py"

    completed = subprocess.run(
        [sys.executable, str(script), "--workspace", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    projects = ProjectStore(tmp_path).iter_projects()

    assert "Created Authorized demo" in completed.stdout
    assert len(projects) == 2
    assert all(len(project.assets) == 3 for project in projects)
    assert all(len(project.voice_references) == 1 for project in projects)
    assert all(len(project.segments) == 1 for project in projects)
