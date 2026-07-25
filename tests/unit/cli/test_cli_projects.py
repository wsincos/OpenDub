from pathlib import Path

from typer.testing import CliRunner

from opendub.cli.app import app
from opendub.storage.project_store import ProjectStore

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_cli_creates_a_project_in_explicit_workspace(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["create", "Authorized demo", "--workspace", str(tmp_path)])

    assert result.exit_code == 0
    assert "Authorized demo" in result.stdout


def test_cli_doctor_emits_machine_readable_json(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["doctor", "--workspace", str(tmp_path), "--json"])

    assert result.exit_code == 0
    assert '"ready"' in result.stdout


def test_cli_init_creates_local_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    result = CliRunner().invoke(app, ["init", "--workspace", str(workspace)])

    assert result.exit_code == 0
    assert workspace.is_dir()
    assert "Initialized" in result.stdout


def test_cli_render_describes_the_accepted_candidate_export_command() -> None:
    result = CliRunner().invoke(app, ["render", "--help"])

    assert result.exit_code == 0
    assert "accepted candidate" in result.stdout.lower()


def test_cli_evaluate_reports_a_missing_candidate_with_a_stable_error(tmp_path: Path) -> None:
    project = ProjectStore(tmp_path).create("Evaluation command")

    result = CliRunner().invoke(
        app, ["evaluate", project.id, "missing", "--workspace", str(tmp_path)]
    )

    assert result.exit_code == 1
    assert "ASSET_NOT_FOUND" in result.output


def test_cli_validates_the_public_method_atlas_content() -> None:
    result = CliRunner().invoke(
        app, ["atlas", "validate", "--content", str(REPOSITORY_ROOT / "content")]
    )

    assert result.exit_code == 0
    assert "3 method manifests validated" in result.output
