#!/usr/bin/env python3
"""Validate the OpenDub upstream provenance registry."""

from __future__ import annotations

import sys
from pathlib import Path

from opendub.models.audit import validate_upstream_registry


def main() -> int:
    registry = Path(__file__).resolve().parents[1] / "config" / "model-registry" / "upstreams.yaml"
    result = validate_upstream_registry(registry)
    if result.is_valid:
        print(f"Registry is valid: {registry}")
        return 0

    print(f"Registry has {len(result.errors)} error(s):", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
