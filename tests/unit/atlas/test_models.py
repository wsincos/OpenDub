from __future__ import annotations

import pytest

from opendub.atlas.models import AtlasValidationError, MethodManifest, ReplayBundle


def valid_method_payload() -> dict[str, object]:
    return {
        "schema_version": "opendub.method/v1",
        "id": "galaxycong/hpmdubbing",
        "slug": "hpmdubbing",
        "title": "HPMDubbing",
        "short_title": "HPM",
        "conference": "CVPR",
        "year": 2023,
        "question": {"zh_cn": "如何让视觉约束韵律？", "en": "How does video constrain prosody?"},
        "contribution": {"zh_cn": "分层韵律", "en": "Hierarchical prosody"},
        "paper": {"title": "Paper", "url": "https://example.com/paper"},
        "source": {"repository": "https://github.com/GalaxyCong/HPMDubbing", "commit": "a" * 40, "license": "MIT"},
        "runtime_status": "unavailable",
        "content_modes": ["concept"],
        "required_inputs": ["video", "text", "reference_speech"],
        "optional_controls": [],
        "signals": [
            {
                "id": "prosody.duration",
                "type": "prosody.duration",
                "label": {"zh_cn": "时长", "en": "Duration"},
                "time_binding": "intervals",
                "renderer": "duration",
                "explanation": {"zh_cn": "音素时长", "en": "Phoneme duration"},
            }
        ],
        "graph": {
            "nodes": [
                {
                    "id": "video",
                    "label": {"zh_cn": "视频", "en": "Video"},
                    "short_label": "Video",
                    "kind": "input",
                    "summary": {"zh_cn": "视频", "en": "Video"},
                    "solves": {"zh_cn": "输入", "en": "Input"},
                    "consumes": [],
                    "produces": ["prosody.duration"],
                    "paper_refs": [{"section": "1", "url": "https://example.com/paper#1"}],
                    "code_refs": [],
                    "visualization_slots": ["prosody.duration"],
                },
                {
                    "id": "speech",
                    "label": {"zh_cn": "语音", "en": "Speech"},
                    "short_label": "Speech",
                    "kind": "output",
                    "summary": {"zh_cn": "输出", "en": "Output"},
                    "solves": {"zh_cn": "输出", "en": "Output"},
                    "consumes": ["prosody.duration"],
                    "produces": [],
                    "paper_refs": [{"section": "1", "url": "https://example.com/paper#1"}],
                    "code_refs": [],
                    "visualization_slots": [],
                },
            ],
            "edges": [
                {
                    "id": "video-to-speech",
                    "source": "video",
                    "target": "speech",
                    "signal_ids": ["prosody.duration"],
                }
            ],
            "groups": [],
            "overview_path": ["video", "speech"],
            "layout": "left-to-right",
        },
        "chapters": [],
        "citations": [],
    }


def valid_replay_payload() -> dict[str, object]:
    return {
        "schema_version": "opendub.replay/v1",
        "id": "demo-hpm-v1",
        "case_id": "authorized-demo",
        "method_id": "galaxycong/hpmdubbing",
        "created_at": "2026-07-26T00:00:00Z",
        "provenance": {"mode": "historical_demo", "parameters": {}, "limitations": []},
        "rights": {
            "video_source": "self_created",
            "voice_source": "self_recorded",
            "text_source": "self_created",
            "public_display_allowed": True,
            "redistribution_allowed": True,
            "evidence_path": "rights.md",
            "reviewer": "reviewer",
            "reviewed_at": "2026-07-26T00:00:00Z",
        },
        "output_speech": {
            "path": "outputs/speech.wav",
            "media_type": "audio/wav",
            "byte_size": 12,
            "sha256": "b" * 64,
        },
        "signals": [
            {
                "signal_id": "prosody.duration",
                "mode": "replay",
                "illustrative": False,
                "asset": {
                    "path": "signals/duration.json",
                    "media_type": "application/json",
                    "byte_size": 10,
                    "sha256": "c" * 64,
                },
                "time_base": {"kind": "intervals"},
            }
        ],
        "metrics": [],
    }


def test_method_rejects_edge_to_unknown_node() -> None:
    payload = valid_method_payload()
    graph = payload["graph"]
    assert isinstance(graph, dict)
    edges = graph["edges"]
    assert isinstance(edges, list)
    edge = edges[0]
    assert isinstance(edge, dict)
    edge["target"] = "missing"

    with pytest.raises(AtlasValidationError, match="ATLAS_EDGE_TARGET_MISSING"):
        MethodManifest.model_validate(payload)


def test_replay_rejects_illustrative_signal() -> None:
    payload = valid_replay_payload()
    signals = payload["signals"]
    assert isinstance(signals, list)
    signal = signals[0]
    assert isinstance(signal, dict)
    signal["illustrative"] = True

    with pytest.raises(AtlasValidationError, match="ATLAS_REPLAY_ILLUSTRATIVE"):
        ReplayBundle.model_validate(payload)
