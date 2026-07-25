from __future__ import annotations

import json
from pathlib import Path

from opendub.atlas.validation import validate_content

from .test_models import valid_method_payload


def write_method(root: Path, payload: dict[str, object]) -> None:
    method_dir = root / "methods" / "hpmdubbing"
    method_dir.mkdir(parents=True)
    (method_dir / "method.json").write_text(json.dumps(payload), encoding="utf-8")


def test_validation_reports_unknown_method_edge(tmp_path: Path) -> None:
    payload = valid_method_payload()
    graph = payload["graph"]
    assert isinstance(graph, dict)
    edges = graph["edges"]
    assert isinstance(edges, list)
    edge = edges[0]
    assert isinstance(edge, dict)
    edge["target"] = "missing"
    write_method(tmp_path, payload)

    report = validate_content(tmp_path)

    assert report.valid is False
    assert report.issues[0].code == "ATLAS_EDGE_TARGET_MISSING"


def test_validation_accepts_a_complete_method_manifest(tmp_path: Path) -> None:
    write_method(tmp_path, valid_method_payload())

    report = validate_content(tmp_path)

    assert report.valid is True
    assert report.method_count == 1
