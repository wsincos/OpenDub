from __future__ import annotations

import json
from pathlib import Path

import pytest

from opendub.atlas.models import MethodManifest
from opendub.atlas.validation import validate_content

CONTENT_ROOT = Path(__file__).resolve().parents[3] / "content"


@pytest.mark.parametrize(
    ("method_id", "required_nodes"),
    [
        ("galaxycong/hpmdubbing", {"lip_duration", "face_affect", "scene_emotion"}),
        ("galaxycong/styledubber", {"mpa", "pla", "usl"}),
        ("galaxycong/emodubber", {"lpa", "pe", "speaker_identity", "fuec", "pngm"}),
    ],
)
def test_core_method_manifest_preserves_its_required_components(
    method_id: str, required_nodes: set[str]
) -> None:
    manifests = [
        MethodManifest.model_validate(json.loads(path.read_text(encoding="utf-8")))
        for path in sorted((CONTENT_ROOT / "methods").glob("*/method.json"))
    ]
    method = next(manifest for manifest in manifests if manifest.id == method_id)

    assert required_nodes <= {node.id for node in method.graph.nodes}
    assert all(node.paper_refs for node in method.graph.nodes)
    assert method.graph.overview_path[-1] == "dubbed_speech"


def test_three_core_method_manifests_validate_as_a_single_atlas() -> None:
    report = validate_content(CONTENT_ROOT)

    assert report.valid is True
    assert report.method_count == 3
