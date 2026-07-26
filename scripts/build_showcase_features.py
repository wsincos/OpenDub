#!/usr/bin/env python3
"""Copy approved showcase media and derive traceable browser display features."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import zlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from opendub.showcase.features import AudioFeatures, analyze_pcm
from opendub.showcase.manifest import load_case_manifest
from opendub.showcase.verification import verify_public_case


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, type=Path, help="Approved showcase case manifest.")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Public case directory, e.g. .../showcases/v2/human-0.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root used to resolve manifest source_path values.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Check source media, public copies, features, and provenance without rewriting files.",
    )
    args = parser.parse_args()
    case_path = args.case.resolve()
    output_directory = args.output.resolve()
    repo_root = args.repo_root.resolve()
    if args.verify_only:
        verify_public_case(case_path, output_directory, repo_root)
    else:
        build_case(case_path, output_directory, repo_root)
    return 0


def build_case(case_path: Path, output_directory: Path, repo_root: Path) -> None:
    """Copy one authorized case and write features derived from every source artifact."""
    case = load_case_manifest(case_path)
    payload = _read_json(case_path)
    artifacts = payload["artifacts"]
    if not isinstance(artifacts, list):
        raise ValueError("artifacts must be a list")
    output_directory.mkdir(parents=True, exist_ok=True)
    features_directory = output_directory / "features"
    features_directory.mkdir(parents=True, exist_ok=True)
    ffmpeg_version = _ffmpeg_version()
    produced: list[dict[str, object]] = []

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("artifact must be an object")
        source = _resolve_source(repo_root, artifact)
        expected_hash = artifact.get("sha256")
        actual_hash = _sha256(source)
        if actual_hash != expected_hash:
            raise ValueError(f"source SHA-256 mismatch for {source}")
        destination = output_directory / _required_string(artifact, "path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        samples, sample_rate = _decode_audio(source)
        features = analyze_pcm(samples, sample_rate=sample_rate)
        feature_name = destination.stem
        feature_json = features_directory / f"{feature_name}.json"
        feature_png = features_directory / f"{feature_name}.mel.png"
        feature_payload = _feature_payload(
            case_id=case.case_id,
            artifact=artifact,
            source_hash=actual_hash,
            sample_rate=sample_rate,
            features=features,
            ffmpeg_version=ffmpeg_version,
        )
        _write_json(feature_json, feature_payload)
        _write_mel_png(feature_png, features.mel)
        record: dict[str, object] = {
            "artifact_path": destination.name,
            "artifact_sha256": _sha256(destination),
            "feature_path": feature_json.relative_to(output_directory).as_posix(),
            "feature_sha256": _sha256(feature_json),
            "mel_png_path": feature_png.relative_to(output_directory).as_posix(),
            "mel_png_sha256": _sha256(feature_png),
        }
        if artifact.get("role") == "ground_truth":
            poster = output_directory / "poster.jpg"
            _write_poster(source, poster)
            record["poster_path"] = poster.relative_to(output_directory).as_posix()
            record["poster_sha256"] = _sha256(poster)
        produced.append(record)

    _write_json(
        output_directory / "provenance.json",
        {
            "schema_version": "opendub.showcase-build/v1",
            "case_id": case.case_id,
            "content_status": case.content_status,
            "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "generator": "scripts/build_showcase_features.py",
            "ffmpeg_version": ffmpeg_version,
            "produced": produced,
        },
    )


def _resolve_source(repo_root: Path, artifact: dict[str, Any]) -> Path:
    source_path = Path(_required_string(artifact, "source_path"))
    if source_path.is_absolute() or ".." in source_path.parts:
        raise ValueError("source_path must be repository-relative")
    source = repo_root / source_path
    if not source.is_file():
        raise ValueError(f"source media does not exist: {source}")
    return source


def _decode_audio(source: Path) -> tuple[np.ndarray, int]:
    sample_rate = 16_000
    result = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(source),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "f32le",
            "pipe:1",
        ],
        check=True,
        capture_output=True,
    )
    return np.frombuffer(result.stdout, dtype=np.float32).copy(), sample_rate


def _feature_payload(
    *,
    case_id: str,
    artifact: dict[str, Any],
    source_hash: str,
    sample_rate: int,
    features: AudioFeatures,
    ffmpeg_version: str,
) -> dict[str, object]:
    return {
        "schema_version": "opendub.audio-features/v1",
        "case_id": case_id,
        "artifact": {
            "role": _required_string(artifact, "role"),
            "method_id": artifact.get("method_id"),
            "source_path": _required_string(artifact, "source_path"),
            "source_sha256": source_hash,
        },
        "analysis": {
            "decoder": "ffmpeg PCM f32le mono",
            "ffmpeg_version": ffmpeg_version,
            "sample_rate_hz": sample_rate,
            "waveform_bins": len(features.waveform_peaks),
            "frame_size": 1024,
            "hop_size": 256,
            "mel_bands": len(features.mel),
            "f0_range_hz": [70, 400],
        },
        "duration_seconds": features.duration_seconds,
        "waveform_peaks": list(features.waveform_peaks),
        "times_seconds": list(features.times_seconds),
        "energy": list(features.energy),
        "f0_hz": list(features.f0_hz),
        "mel": [list(row) for row in features.mel],
    }


def _write_mel_png(path: Path, mel: tuple[tuple[float, ...], ...]) -> None:
    rows = np.asarray(mel, dtype=np.float32)
    if rows.ndim != 2 or rows.size == 0:
        raise ValueError("mel must be a non-empty two-dimensional array")
    image = np.flipud(np.clip(rows * 255, 0, 255).astype(np.uint8))
    red = image
    green = np.minimum(255, image * 1.45).astype(np.uint8)
    blue = np.minimum(255, 255 - image // 2).astype(np.uint8)
    rgb = np.dstack((red, green, blue))
    raw = b"".join(b"\x00" + row.tobytes() for row in rgb)
    png = b"\x89PNG\r\n\x1a\n" + _png_chunk(
        b"IHDR", struct.pack(">IIBBBBB", rgb.shape[1], rgb.shape[0], 8, 2, 0, 0, 0)
    ) + _png_chunk(b"IDAT", zlib.compress(raw, 9)) + _png_chunk(b"IEND", b"")
    path.write_bytes(png)


def _write_poster(source: Path, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            "0.6",
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(destination),
        ],
        check=True,
        capture_output=True,
    )


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = struct.pack(">I", zlib.crc32(kind + payload))
    return struct.pack(">I", len(payload)) + kind + payload + checksum


def _ffmpeg_version() -> str:
    result = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
    return result.stdout.splitlines()[0]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("showcase manifest must be a JSON object")
    return value


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
