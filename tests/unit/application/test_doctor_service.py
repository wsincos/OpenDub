from pathlib import Path

from opendub.application.doctor_service import run_doctor


def test_doctor_reports_local_workspace_ffmpeg_and_registry(tmp_path: Path) -> None:
    registry = tmp_path / "upstreams.yaml"
    registry.write_text(
        "schema_version: opendub.upstream-registry/v1\nmodels: []\n",
        encoding="utf-8",
    )

    report = run_doctor(
        workspace=tmp_path / "workspace",
        registry_path=registry,
        run_command=lambda command: command == ("ffmpeg", "-version"),
    )

    assert report.ready is True
    assert {check.id for check in report.checks} == {"workspace.writable", "ffmpeg", "registry"}


def test_doctor_is_not_ready_when_ffmpeg_is_missing(tmp_path: Path) -> None:
    registry = tmp_path / "upstreams.yaml"
    registry.write_text(
        "schema_version: opendub.upstream-registry/v1\nmodels: []\n",
        encoding="utf-8",
    )

    report = run_doctor(
        workspace=tmp_path / "workspace",
        registry_path=registry,
        run_command=lambda _command: False,
    )

    assert report.ready is False
    assert next(check for check in report.checks if check.id == "ffmpeg").status == "failed"
