from __future__ import annotations

import json
from pathlib import Path

import pytest

from opendub.showcase.manifest import load_case_manifest


def test_load_case_manifest_accepts_an_archived_gallery_case(tmp_path: Path) -> None:
    path = tmp_path / "case.json"
    path.write_text(json.dumps(_valid_manifest()), encoding="utf-8")

    case = load_case_manifest(path)

    assert case.case_id == "human-0"
    assert case.content_status == "archived_research_example"
    assert case.timeline_eligible is False
    assert case.artifacts[1].method_id == "galaxycong/hpmdubbing"


def test_load_case_manifest_rejects_public_media_without_redistribution_permission(
    tmp_path: Path,
) -> None:
    payload = _valid_manifest()
    payload["rights"]["redistribution"] = "not-confirmed"
    path = tmp_path / "case.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="redistribution"):
        load_case_manifest(path)


def test_load_case_manifest_rejects_replay_when_same_input_is_not_verified(tmp_path: Path) -> None:
    payload = _valid_manifest()
    payload["content_status"] = "replay"
    path = tmp_path / "case.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="same_input_across_methods"):
        load_case_manifest(path)


def test_load_case_manifest_rejects_a_public_case_without_an_authorization_record(
    tmp_path: Path,
) -> None:
    payload = _valid_manifest()
    del payload["authorization_record"]
    path = tmp_path / "case.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="authorization_record"):
        load_case_manifest(path)


def _valid_manifest() -> dict[str, object]:
    digest = "a" * 64
    return {
        "schema_version": "opendub.showcase/v1",
        "case_id": "human-0",
        "display_name": "Human portrait case",
        "content_status": "archived_research_example",
        "timeline_eligible": False,
        "rights": {
            "video": "confirmed-by-project-owner",
            "reference_speech": "confirmed-by-project-owner",
            "redistribution": "allowed-for-opendub-v2",
        },
        "authorization_record": {
            "record_path": "docs/rights/showcase-media-rights-v2.md",
            "approver_role": "OpenDub project owner",
            "approved_on": "2026-07-27",
            "public_scope": ["repository", "grant-application-video"],
        },
        "input_contract": {
            "target_text_source": "unavailable-for-gallery-only",
            "target_text": None,
            "ipa_source": "unavailable-for-gallery-only",
            "same_input_across_methods": False,
        },
        "artifacts": [
            {"role": "ground_truth", "path": "gt.mp4", "sha256": digest},
            {
                "role": "method_output",
                "method_id": "galaxycong/hpmdubbing",
                "path": "hpmdubbing.mp4",
                "sha256": digest,
            },
        ],
        "provenance": {
            "method_revision": "historical-result-see-upstream-registry",
            "result_origin": "team-provided historical output",
        },
    }
