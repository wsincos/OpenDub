from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from opendub.showcase.verification import verify_public_case


def test_verify_public_case_accepts_a_public_bundle_without_private_source_media(
    tmp_path: Path,
) -> None:
    case_path, public_directory = _write_case_bundle(tmp_path)
    (tmp_path / "source.mp4").unlink()

    verify_public_case(case_path, public_directory, tmp_path)


def test_verify_public_case_rejects_tampered_public_media(tmp_path: Path) -> None:
    case_path, public_directory = _write_case_bundle(tmp_path)
    (public_directory / "gt.mp4").write_bytes(b"tampered")

    with pytest.raises(ValueError, match="public artifact SHA-256 mismatch"):
        verify_public_case(case_path, public_directory, tmp_path)


def test_verify_public_case_rejects_feature_with_wrong_source_hash(tmp_path: Path) -> None:
    case_path, public_directory = _write_case_bundle(tmp_path)
    feature_path = public_directory / "features" / "gt.json"
    payload = json.loads(feature_path.read_text(encoding="utf-8"))
    payload["artifact"]["source_sha256"] = "0" * 64
    feature_path.write_text(json.dumps(payload), encoding="utf-8")
    provenance_path = public_directory / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["produced"][0]["feature_sha256"] = _sha256(feature_path)
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")

    with pytest.raises(ValueError, match="feature source SHA-256 mismatch"):
        verify_public_case(case_path, public_directory, tmp_path)


def _write_case_bundle(root: Path) -> tuple[Path, Path]:
    source = root / "source.mp4"
    source.write_bytes(b"approved media")
    digest = _sha256(source)
    case = {
        "schema_version": "opendub.showcase/v1",
        "case_id": "case-0",
        "display_name": "Case zero",
        "duration_seconds": 1.0,
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
            {
                "role": "ground_truth",
                "path": "gt.mp4",
                "source_path": "source.mp4",
                "sha256": digest,
            }
        ],
        "provenance": {
            "method_revision": "historical-result",
            "result_origin": "team-provided historical output",
        },
    }
    case_path = root / "case.json"
    case_path.write_text(json.dumps(case), encoding="utf-8")

    public_directory = root / "public"
    features = public_directory / "features"
    features.mkdir(parents=True)
    (public_directory / "gt.mp4").write_bytes(source.read_bytes())
    (public_directory / "poster.jpg").write_bytes(b"poster")
    feature_payload = {
        "schema_version": "opendub.audio-features/v1",
        "case_id": "case-0",
        "artifact": {"source_sha256": digest},
    }
    feature_path = features / "gt.json"
    feature_path.write_text(json.dumps(feature_payload), encoding="utf-8")
    mel_path = features / "gt.mel.png"
    mel_path.write_bytes(b"mel")
    provenance = {
        "schema_version": "opendub.showcase-build/v1",
        "case_id": "case-0",
        "content_status": "archived_research_example",
        "produced": [
            {
                "artifact_path": "gt.mp4",
                "artifact_sha256": digest,
                "feature_path": "features/gt.json",
                "feature_sha256": _sha256(feature_path),
                "mel_png_path": "features/gt.mel.png",
                "mel_png_sha256": _sha256(mel_path),
                "poster_path": "poster.jpg",
                "poster_sha256": _sha256(public_directory / "poster.jpg"),
            }
        ],
    }
    (public_directory / "provenance.json").write_text(json.dumps(provenance), encoding="utf-8")
    return case_path, public_directory


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
