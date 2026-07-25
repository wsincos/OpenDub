from pathlib import Path

from opendub.models.audit import validate_upstream_registry


def write_registry(path: Path, *, maturity: str, commit: str, checksum: str) -> Path:
    registry = path / "upstreams.yaml"
    registry.write_text(
        f"""models:
  - id: test/model
    display_name: Test Model
    maturity: {maturity}
    source:
      repository: https://example.com/test/model
      commit: {commit}
      license: MIT
    artifacts:
      - role: acoustic_model
        sha256: {checksum}
""",
        encoding="utf-8",
    )
    return registry


def test_registry_rejects_releasable_model_without_commit(tmp_path: Path) -> None:
    registry = write_registry(
        tmp_path,
        maturity="experimental",
        commit="",
        checksum="a" * 64,
    )

    result = validate_upstream_registry(registry)

    assert "test/model: source.commit is required" in result.errors


def test_registry_rejects_stable_model_without_weight_checksum(tmp_path: Path) -> None:
    registry = write_registry(
        tmp_path,
        maturity="stable",
        commit="a" * 40,
        checksum="",
    )

    result = validate_upstream_registry(registry)

    assert "test/model: artifacts[0].sha256 is required" in result.errors


def test_registry_allows_planned_model_without_release_artifacts(tmp_path: Path) -> None:
    registry = write_registry(
        tmp_path,
        maturity="planned",
        commit="",
        checksum="",
    )

    result = validate_upstream_registry(registry)

    assert result.errors == ()


def test_registry_rejects_releasable_model_without_adapter_admission_evidence(
    tmp_path: Path,
) -> None:
    registry = write_registry(
        tmp_path,
        maturity="experimental",
        commit="a" * 40,
        checksum="b" * 64,
    )

    result = validate_upstream_registry(registry)

    assert "test/model: admission is required" in result.errors


def test_registry_allows_releasable_model_with_complete_adapter_admission(tmp_path: Path) -> None:
    registry = write_registry(
        tmp_path,
        maturity="experimental",
        commit="a" * 40,
        checksum="b" * 64,
    )
    registry.write_text(
        registry.read_text(encoding="utf-8")
        + """    admission:
      adapter_version: 0.1.0
      input_contract: docs/adapters/test-model-input.md
      real_smoke_report: reports/test-model-smoke.md
""",
        encoding="utf-8",
    )

    result = validate_upstream_registry(registry)

    assert result.errors == ()
