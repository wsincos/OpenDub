from dataclasses import replace

from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.pipeline.planner import GenerationInputs, PipelinePlanner


def _inputs(*, seed: int = 7, text: str = "Keep the scene timing.") -> GenerationInputs:
    return GenerationInputs(
        project_id=new_id(),
        segment=DubbingSegment(
            range=TimeRange(start_us=0, end_us=1_000_000),
            text=text,
            language="en",
            character_id=new_id(),
            voice_reference_id=new_id(),
            emotion=EmotionSpec(label="neutral", intensity=0.5),
            adapter_id="example/adapter",
            status="ready",
        ),
        video_sha256="a" * 64,
        voice_sha256="b" * 64,
        adapter_version="1.2.3",
        model_id="example/model",
        weights_sha256="c" * 64,
        seed=seed,
    )


def test_generation_plan_changes_only_downstream_cache_keys_for_a_new_seed() -> None:
    planner = PipelinePlanner()

    inputs = _inputs(seed=7)
    baseline = planner.plan_generation(inputs)
    changed_seed = planner.plan_generation(replace(inputs, seed=8))

    assert baseline.stage("prepare").cache_key == changed_seed.stage("prepare").cache_key
    assert baseline.stage("generate").cache_key != changed_seed.stage("generate").cache_key
    assert baseline.stage("postprocess").cache_key != changed_seed.stage("postprocess").cache_key
    assert baseline.stage("evaluate").cache_key != changed_seed.stage("evaluate").cache_key


def test_generation_plan_invalidates_every_stage_when_dialogue_changes() -> None:
    planner = PipelinePlanner()

    inputs = _inputs(text="First line.")
    revised_segment = inputs.segment.model_copy(update={"text": "Revised line."})
    baseline = planner.plan_generation(inputs)
    changed_text = planner.plan_generation(replace(inputs, segment=revised_segment))

    assert [stage.cache_key for stage in baseline.stages] != [
        stage.cache_key for stage in changed_text.stages
    ]
