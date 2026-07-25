"""Build reproducible, dependency-ordered plans for one dubbing segment."""

from __future__ import annotations

from dataclasses import dataclass

from opendub.domain.segments import DubbingSegment
from opendub.pipeline.cache import stage_cache_key
from opendub.pipeline.stages import PipelineStage, PipelineStageName


@dataclass(frozen=True)
class GenerationInputs:
    """All externally meaningful inputs that can affect a segment generation result."""

    project_id: str
    segment: DubbingSegment
    video_sha256: str
    voice_sha256: str
    adapter_version: str
    model_id: str
    weights_sha256: str
    seed: int


@dataclass(frozen=True)
class GenerationPlan:
    """An ordered plan whose cache keys capture every downstream dependency."""

    project_id: str
    segment_id: str
    segment_revision: int
    stages: tuple[PipelineStage, ...]

    def stage(self, name: PipelineStageName) -> PipelineStage:
        """Return a declared stage by name without exposing ordering assumptions to callers."""
        for stage in self.stages:
            if stage.name == name:
                return stage
        raise ValueError(f"Generation plan does not define {name!r}.")


class PipelinePlanner:
    """Derive a stable four-stage execution plan from explicitly supplied provenance."""

    _VERSION = "opendub.pipeline/v1"

    def plan_generation(self, inputs: GenerationInputs) -> GenerationPlan:
        """Plan preprocess, synthesis, postprocess, and evaluation with chained cache keys."""
        segment = inputs.segment
        prepare = PipelineStage(
            name="prepare",
            cache_key=stage_cache_key(
                {
                    "pipeline": self._VERSION,
                    "stage": "prepare",
                    "video_sha256": inputs.video_sha256,
                    "voice_sha256": inputs.voice_sha256,
                    "segment": {
                        "id": segment.id,
                        "revision": segment.revision,
                        "range": {
                            "start_us": segment.range.start_us,
                            "end_us": segment.range.end_us,
                        },
                        "text": segment.text,
                        "language": segment.language,
                        "voice_reference_id": segment.voice_reference_id,
                        "emotion": segment.emotion.model_dump(),
                    },
                    "adapter_id": segment.adapter_id,
                    "adapter_version": inputs.adapter_version,
                }
            ),
        )
        generate = PipelineStage(
            name="generate",
            cache_key=stage_cache_key(
                {
                    "pipeline": self._VERSION,
                    "stage": "generate",
                    "prepare_cache_key": prepare.cache_key,
                    "model_id": inputs.model_id,
                    "weights_sha256": inputs.weights_sha256,
                    "seed": inputs.seed,
                }
            ),
        )
        postprocess = PipelineStage(
            name="postprocess",
            cache_key=stage_cache_key(
                {
                    "pipeline": self._VERSION,
                    "stage": "postprocess",
                    "generate_cache_key": generate.cache_key,
                    "target_duration_us": segment.range.duration_us,
                }
            ),
        )
        evaluate = PipelineStage(
            name="evaluate",
            cache_key=stage_cache_key(
                {
                    "pipeline": self._VERSION,
                    "stage": "evaluate",
                    "postprocess_cache_key": postprocess.cache_key,
                    "metric_suite": "opendub.deterministic-audio/v1",
                }
            ),
        )
        return GenerationPlan(
            project_id=inputs.project_id,
            segment_id=segment.id,
            segment_revision=segment.revision,
            stages=(prepare, generate, postprocess, evaluate),
        )
