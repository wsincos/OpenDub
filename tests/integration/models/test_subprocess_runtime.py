from __future__ import annotations

import sys
from pathlib import Path

import pytest

from opendub.domain.errors import DomainError
from opendub.models.runtime import SubprocessRuntime
from opendub.pipeline.cancellation import CancellationToken


def write_worker(path: Path) -> None:
    path.write_text(
        """import json
import sys
for line in sys.stdin:
    request = json.loads(line)
    if request["type"] == "handshake":
        print(json.dumps({"type": "environment", "ready": True, "checks": ["python"]}), flush=True)
    elif request["type"] == "generate":
        print(
            json.dumps({"type": "progress", "stage": "model.inference", "progress": 0.5}),
            flush=True,
        )
        print(json.dumps({"type": "result", "payload": {"audio": "candidate.wav"}}), flush=True)
""",
        encoding="utf-8",
    )


def test_runtime_handshake_and_generation_use_json_lines(tmp_path: Path) -> None:
    worker = tmp_path / "worker.py"
    write_worker(worker)
    runtime = SubprocessRuntime((sys.executable, str(worker)))

    report = runtime.prepare()
    result = runtime.generate({"segment_id": "safe-id"}, cancellation=CancellationToken())

    assert report.ready is True
    assert result.payload == {"audio": "candidate.wav"}
    assert result.events[0].stage == "model.inference"


def test_runtime_refuses_generation_after_cancellation(tmp_path: Path) -> None:
    worker = tmp_path / "worker.py"
    write_worker(worker)
    cancellation = CancellationToken()
    cancellation.cancel()

    with pytest.raises(DomainError, match="JOB_CANCELLED"):
        SubprocessRuntime((sys.executable, str(worker))).generate({}, cancellation=cancellation)
