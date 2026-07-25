"""A JSON Lines subprocess boundary for dependency-isolated model adapters."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from opendub.domain.errors import DomainError
from opendub.pipeline.cancellation import CancellationToken


@dataclass(frozen=True)
class EnvironmentReport:
    """A model worker's readiness report from the required startup handshake."""

    ready: bool
    checks: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeEvent:
    """A structured progress event emitted by an isolated worker."""

    stage: str
    progress: float | None


@dataclass(frozen=True)
class RuntimeResult:
    """The final result and every reported progress event for one request."""

    payload: dict[str, object]
    events: tuple[RuntimeEvent, ...]


class SubprocessRuntime:
    """Start an adapter worker with an argument array and exchange JSON Lines."""

    def __init__(self, command: Sequence[str], *, timeout_seconds: float = 300.0) -> None:
        if not command:
            raise ValueError("runtime command must not be empty")
        self.command = tuple(command)
        self.timeout_seconds = timeout_seconds

    def prepare(self) -> EnvironmentReport:
        """Run the mandatory worker handshake and return its environment report."""
        messages = self._exchange({"type": "handshake"})
        environment = next(
            (message for message in messages if message.get("type") == "environment"),
            None,
        )
        if environment is None:
            raise DomainError(
                code="MODEL_NOT_READY",
                message="Model worker did not return an environment report.",
            )
        ready = environment.get("ready")
        checks = environment.get("checks")
        if (
            not isinstance(ready, bool)
            or not isinstance(checks, list)
            or not all(isinstance(check, str) for check in checks)
        ):
            raise DomainError(
                code="MODEL_NOT_READY",
                message="Model worker returned an invalid environment report.",
            )
        return EnvironmentReport(ready=ready, checks=tuple(checks))

    def generate(
        self,
        payload: dict[str, object],
        *,
        cancellation: CancellationToken,
    ) -> RuntimeResult:
        """Run a generation request unless cooperative cancellation was already requested."""
        _raise_if_cancelled(cancellation)
        messages = self._exchange({"type": "generate", "payload": payload})
        _raise_if_cancelled(cancellation)
        events = tuple(
            _parse_progress(message) for message in messages if message.get("type") == "progress"
        )
        error = next((message for message in messages if message.get("type") == "error"), None)
        if error is not None:
            message = error.get("message")
            raise DomainError(
                code="INTERNAL_ERROR",
                message=message if isinstance(message, str) else "Model worker reported an error.",
            )
        result = next((message for message in messages if message.get("type") == "result"), None)
        if result is None or not isinstance(result.get("payload"), dict):
            raise DomainError(
                code="INTERNAL_ERROR",
                message="Model worker did not return a result.",
            )
        return RuntimeResult(payload=result["payload"], events=events)

    def _exchange(self, request: dict[str, object]) -> tuple[dict[str, Any], ...]:
        encoded = f"{json.dumps(request, sort_keys=True)}\n"
        try:
            completed = subprocess.run(
                self.command,
                input=encoded,
                capture_output=True,
                text=True,
                check=False,
                shell=False,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            raise DomainError(code="MODEL_NOT_READY", message="Model worker timed out.") from error
        if completed.returncode != 0:
            raise DomainError(
                code="INTERNAL_ERROR",
                message=completed.stderr[-4_000:] or "Model worker exited unsuccessfully.",
            )
        messages: list[dict[str, Any]] = []
        for line in completed.stdout.splitlines():
            try:
                decoded = json.loads(line)
            except json.JSONDecodeError as error:
                raise DomainError(
                    code="INTERNAL_ERROR",
                    message="Model worker emitted invalid JSON Lines.",
                ) from error
            if not isinstance(decoded, dict) or not isinstance(decoded.get("type"), str):
                raise DomainError(
                    code="INTERNAL_ERROR",
                    message="Model worker emitted an invalid message.",
                )
            messages.append(decoded)
        return tuple(messages)


def _parse_progress(message: dict[str, Any]) -> RuntimeEvent:
    stage = message.get("stage")
    progress = message.get("progress")
    if not isinstance(stage, str):
        raise DomainError(code="INTERNAL_ERROR", message="Model worker progress has no stage.")
    if progress is not None and (
        isinstance(progress, bool) or not isinstance(progress, (int, float))
    ):
        raise DomainError(code="INTERNAL_ERROR", message="Model worker progress is invalid.")
    return RuntimeEvent(stage=stage, progress=float(progress) if progress is not None else None)


def _raise_if_cancelled(cancellation: CancellationToken) -> None:
    if cancellation.cancelled:
        raise DomainError(code="JOB_CANCELLED", message="Generation was cancelled.")
