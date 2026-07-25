from pathlib import Path

from opendub.models.registry import ModelRegistry


def test_registry_discovers_upstream_records_from_structured_yaml(tmp_path: Path) -> None:
    registry_file = tmp_path / "upstreams.yaml"
    registry_file.write_text(
        """schema_version: opendub.upstream-registry/v1
models:
  - id: example/ready
    display_name: Ready model
    maturity: experimental
    source:
      repository: https://example.com/ready
      commit: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      license: Apache-2.0
    artifacts:
      - role: acoustic_model
        sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    admission:
      adapter_version: 0.1.0
      input_contract: docs/adapters/ready-input.md
      real_smoke_report: reports/ready-smoke.md
""",
        encoding="utf-8",
    )

    records = ModelRegistry(registry_file).discover()

    assert len(records) == 1
    assert records[0].id == "example/ready"
    assert records[0].is_releasable is True
