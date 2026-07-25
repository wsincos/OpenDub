"""Execute a generation plan with atomic, retry-safe stage result caching."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from opendub.domain.errors import DomainError
from opendub.pipeline.cancellation import CancellationToken
from opendub.pipeline.planner import GenerationPlan
from opendub.pipeline.stages import PipelineStage, PipelineStageName
from opendub.storage.atomic import atomic_write_text

StageOperation = Callable[["StageExecutionContext"], Mapping[str, object]]


@dataclass(frozen=True)
class StageExecutionContext:
    """Inputs available to exactly one operation without exposing filesystem policy."""

    plan: GenerationPlan
    stage: PipelineStage
    prior_results: Mapping[PipelineStageName, StageExecutionResult]
    cancellation: CancellationToken

    def raise_if_cancelled(self) -> None:
        """Ensure long-running adapters cannot commit output after a cancel request."""
        if self.cancellation.cancelled:
            raise DomainError(code="JOB_CANCELLED", message="Pipeline execution was cancelled.")


@dataclass(frozen=True)
class StageExecutionResult:
    """One decoded stage result together with the source that produced it."""

    stage: PipelineStage
    payload: dict[str, object]
    from_cache: bool


@dataclass(frozen=True)
class PipelineExecutionResult:
    """All completed stage results in plan order."""

    stages: tuple[StageExecutionResult, ...]

    def stage(self, name: PipelineStageName) -> StageExecutionResult:
        """Return the result for a named stage."""
        for result in self.stages:
            if result.stage.name == name:
                return result
        raise ValueError(f"Pipeline execution has no result for {name!r}.")


class PipelineExecutor:
    """Persist only complete JSON stage results under their content-addressed cache keys."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir

    def execute(
        self,
        plan: GenerationPlan,
        *,
        operations: Mapping[PipelineStageName, StageOperation],
        cancellation: CancellationToken,
    ) -> PipelineExecutionResult:
        """Run missing stages in order and reuse only self-consistent cached JSON results."""
        results: dict[PipelineStageName, StageExecutionResult] = {}
        for stage in plan.stages:
            if stage.name not in operations:
                raise DomainError(
                    code="INPUT_INVALID",
                    message=f"No operation was supplied for pipeline stage {stage.name}.",
                )
            if cancellation.cancelled:
                raise DomainError(code="JOB_CANCELLED", message="Pipeline execution was cancelled.")
            cached = self._load_cached(stage)
            if cached is not None:
                results[stage.name] = StageExecutionResult(
                    stage=stage, payload=cached, from_cache=True
                )
                continue
            context = StageExecutionContext(
                plan=plan,
                stage=stage,
                prior_results=results,
                cancellation=cancellation,
            )
            payload = dict(operations[stage.name](context))
            context.raise_if_cancelled()
            self._write_cached(stage, payload)
            results[stage.name] = StageExecutionResult(
                stage=stage, payload=payload, from_cache=False
            )
        return PipelineExecutionResult(stages=tuple(results[stage.name] for stage in plan.stages))

    def _cache_path(self, stage: PipelineStage) -> Path:
        return self.cache_dir / stage.name / f"{stage.cache_key}.json"

    def _load_cached(self, stage: PipelineStage) -> dict[str, object] | None:
        path = self._cache_path(stage)
        if not path.is_file():
            return None
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        payload = record.get("payload") if isinstance(record, dict) else None
        if (
            not isinstance(payload, dict)
            or record.get("stage") != stage.name
            or record.get("cache_key") != stage.cache_key
        ):
            return None
        return payload

    def _write_cached(self, stage: PipelineStage, payload: Mapping[str, object]) -> None:
        try:
            document = json.dumps(
                {"stage": stage.name, "cache_key": stage.cache_key, "payload": payload},
                ensure_ascii=False,
                sort_keys=True,
            )
        except (TypeError, ValueError) as error:
            raise DomainError(
                code="INTERNAL_ERROR",
                message=f"Pipeline stage {stage.name} returned a non-serializable result.",
            ) from error
        atomic_write_text(self._cache_path(stage), f"{document}\n")
