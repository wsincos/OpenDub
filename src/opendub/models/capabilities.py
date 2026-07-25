"""Truthful, machine-readable declarations of each model adapter's behavior."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from opendub.domain.segments import EmotionLabel

Maturity = Literal["stable", "experimental", "planned"]
OutputType = Literal["waveform", "mel"]
RuntimeIsolation = Literal["in_process", "subprocess", "container"]


class ModelCapabilities(BaseModel):
    """Controls an adapter genuinely supports, without optimistic inference."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = "opendub.model-capabilities/v1"
    adapter_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    maturity: Maturity
    languages: tuple[str, ...] = Field(min_length=1)
    requires_video: bool
    requires_face: bool
    requires_lip_roi: bool
    requires_reference_audio: bool
    emotion_labels: tuple[EmotionLabel, ...]
    supports_emotion_strength: bool
    supports_valence_arousal: bool
    supports_style_reference: bool
    supports_duration_control: bool
    output_type: OutputType
    sample_rates: tuple[int, ...] = Field(min_length=1)
    minimum_vram_gb: float | None = Field(default=None, ge=0.0)
    source_license: str = Field(min_length=1)
    weights_license: str = Field(min_length=1)
    runtime_isolation: RuntimeIsolation

    @model_validator(mode="after")
    def validate_declared_controls(self) -> ModelCapabilities:
        if self.supports_emotion_strength and not self.emotion_labels:
            raise ValueError("emotion labels are required for emotion-strength control")
        if self.supports_valence_arousal and not self.emotion_labels:
            raise ValueError("emotion labels are required for valence/arousal control")
        if any(rate <= 0 for rate in self.sample_rates):
            raise ValueError("sample rates must be positive")
        if (
            self.maturity in {"stable", "experimental"}
            and self.weights_license.lower() == "unknown"
        ):
            raise ValueError("releasable adapters require a verified weights license")
        return self
