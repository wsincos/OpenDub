from pathlib import Path

import pytest

from opendub.domain.errors import DomainError
from opendub.pipeline.cancellation import CancellationToken
from opendub.pipeline.executor import PipelineExecutor
from opendub.pipeline.planner import GenerationPlan
from opendub.pipeline.stages import PipelineStage


def _plan() -> GenerationPlan:
    return GenerationPlan(
        project_id="project-1",
        segment_id="segment-1",
        segment_revision=1,
        stages=(
            PipelineStage(name="prepare", cache_key="a" * 64),
            PipelineStage(name="generate", cache_key="b" * 64),
            PipelineStage(name="postprocess", cache_key="c" * 64),
            PipelineStage(name="evaluate", cache_key="d" * 64),
        ),
    )


def test_executor_reuses_verified_stages_after_a_later_failure(tmp_path: Path) -> None:
    calls: list[str] = []
    executor = PipelineExecutor(tmp_path)

    def prepare(_context: object) -> dict[str, object]:
        calls.append("prepare")
        return {"prepared": True}

    def generate(_context: object) -> dict[str, object]:
        calls.append("generate")
        return {"candidate": "generated"}

    def fail_postprocess(_context: object) -> dict[str, object]:
        calls.append("postprocess")
        raise DomainError(code="INTERNAL_ERROR", message="temporary worker failure")

    with pytest.raises(DomainError, match="temporary worker failure"):
        executor.execute(
            _plan(),
            operations={
                "prepare": prepare,
                "generate": generate,
                "postprocess": fail_postprocess,
                "evaluate": lambda _context: {},
            },
            cancellation=CancellationToken(),
        )

    def postprocess(_context: object) -> dict[str, object]:
        calls.append("postprocess-retry")
        return {"audio": "normalized.wav"}

    result = executor.execute(
        _plan(),
        operations={
            "prepare": prepare,
            "generate": generate,
            "postprocess": postprocess,
            "evaluate": lambda _context: {"duration_error_us": 0},
        },
        cancellation=CancellationToken(),
    )

    assert calls == ["prepare", "generate", "postprocess", "postprocess-retry"]
    assert result.stage("prepare").from_cache is True
    assert result.stage("generate").from_cache is True
    assert result.stage("postprocess").from_cache is False
    assert result.stage("evaluate").payload == {"duration_error_us": 0}


def test_executor_does_not_commit_cache_when_cancelled(tmp_path: Path) -> None:
    token = CancellationToken()
    executor = PipelineExecutor(tmp_path)

    def cancel(_context: object) -> dict[str, object]:
        token.cancel()
        return {"would": "be partial"}

    with pytest.raises(DomainError, match="cancelled"):
        executor.execute(
            _plan(),
            operations={
                "prepare": cancel,
                "generate": lambda _context: {},
                "postprocess": lambda _context: {},
                "evaluate": lambda _context: {},
            },
            cancellation=token,
        )

    assert not list(tmp_path.rglob("*.json"))
