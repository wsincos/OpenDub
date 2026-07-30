from __future__ import annotations

from pathlib import Path

from opendub.showcase.manifest import load_case_manifest
from opendub.showcase.verification import verify_public_case

REPO_ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = REPO_ROOT / "content/showcases/v4/case-04.json"
PUBLIC_DIRECTORY = REPO_ROOT / "apps/web/public/showcases/v4/case-04"


def test_case_04_is_an_authorized_archived_scene_with_the_declared_method_mapping() -> None:
    case = load_case_manifest(CASE_PATH)

    assert case.case_id == "case-04"
    assert case.display_name == "Presenter and display scene"
    assert case.duration_seconds == 7.8
    assert case.content_status == "archived_research_example"
    assert case.timeline_eligible is False
    assert [(artifact.role, artifact.path, artifact.method_id) for artifact in case.artifacts] == [
        ("ground_truth", "gt.mp4", None),
        ("method_output", "hpmdubbing.mp4", "galaxycong/hpmdubbing"),
        ("method_output", "styledubber.mp4", "galaxycong/styledubber"),
        ("method_output", "emodubber.mp4", "galaxycong/emodubber"),
    ]


def test_case_04_public_media_features_and_contact_frames_are_traceable() -> None:
    verify_public_case(CASE_PATH, PUBLIC_DIRECTORY, REPO_ROOT)

    for artifact_name in ("gt", "hpmdubbing", "styledubber", "emodubber"):
        for index in range(5):
            assert (PUBLIC_DIRECTORY / "contacts" / f"{artifact_name}-{index}.jpg").is_file()
