import pytest
from pydantic import ValidationError

from opendub.models.capabilities import ModelCapabilities


def valid_capabilities(**updates: object) -> ModelCapabilities:
    values: dict[str, object] = {
        "adapter_id": "opendub.mock",
        "display_name": "Mock Adapter",
        "version": "0.1.0",
        "maturity": "experimental",
        "languages": ("en", "zh"),
        "requires_video": True,
        "requires_face": False,
        "requires_lip_roi": False,
        "requires_reference_audio": True,
        "emotion_labels": ("neutral", "happy"),
        "supports_emotion_strength": True,
        "supports_valence_arousal": False,
        "supports_style_reference": False,
        "supports_duration_control": True,
        "output_type": "waveform",
        "sample_rates": (24_000,),
        "minimum_vram_gb": 8.0,
        "source_license": "Apache-2.0",
        "weights_license": "research-only",
        "runtime_isolation": "subprocess",
    }
    values.update(updates)
    return ModelCapabilities.model_validate(values)


def test_capabilities_require_emotion_labels_for_emotion_strength() -> None:
    with pytest.raises(ValidationError, match="emotion labels"):
        valid_capabilities(emotion_labels=(), supports_emotion_strength=True)


def test_capabilities_require_valence_arousal_support_to_expose_controls() -> None:
    with pytest.raises(ValidationError, match="valence/arousal"):
        valid_capabilities(
            emotion_labels=(),
            supports_emotion_strength=False,
            supports_valence_arousal=True,
        )


def test_valid_capabilities_are_immutable() -> None:
    capabilities = valid_capabilities()

    with pytest.raises(ValidationError):
        capabilities.version = "unreviewed"  # type: ignore[misc]
