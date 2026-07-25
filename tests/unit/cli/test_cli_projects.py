from pathlib import Path

from typer.testing import CliRunner

from opendub.cli.app import app


def test_cli_creates_a_project_in_explicit_workspace(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["create", "Authorized demo", "--workspace", str(tmp_path)])

    assert result.exit_code == 0
    assert "Authorized demo" in result.stdout
