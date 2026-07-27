from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validator():
    path = Path(__file__).parents[3] / "scripts" / "verify_v3_audio_map.py"
    spec = importlib.util.spec_from_file_location("verify_v3_audio_map", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_v3_source_map_has_every_required_browser_capture() -> None:
    root = Path(__file__).parents[3]
    validator = _load_validator()

    assert validator.verify_audio_map(
        root / "docs/grant/video/v3/source-audio-map.json", root, True
    ) == []
