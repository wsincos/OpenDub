from __future__ import annotations

from pathlib import Path

from opendub.showcase.manifest import load_case_manifest
from opendub.showcase.verification import verify_public_case

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = REPO_ROOT / "content/showcases/v3/case-03.json"
PUBLIC_DIRECTORY = REPO_ROOT / "apps/web/public/showcases/v3/case-03"


def test_case_03_is_an_archived_listening_bundle_with_the_declared_method_mapping() -> None:
    case = load_case_manifest(CASE_PATH)

    assert case.case_id == "case-03"
    assert case.display_name == "Animated cinematic scene"
    assert case.content_status == "archived_research_example"
    assert case.timeline_eligible is False
    assert [(artifact.role, artifact.path, artifact.method_id) for artifact in case.artifacts] == [
        ("ground_truth", "gt.mp4", None),
        ("method_output", "hpmdubbing.mp4", "galaxycong/hpmdubbing"),
        ("method_output", "styledubber.mp4", "galaxycong/styledubber"),
        ("method_output", "emodubber.mp4", "galaxycong/emodubber"),
    ]


def test_case_03_public_media_and_derived_features_are_traceable() -> None:
    verify_public_case(CASE_PATH, PUBLIC_DIRECTORY, REPO_ROOT)
