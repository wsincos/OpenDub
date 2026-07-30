#!/usr/bin/env python3
"""Export OpenDub's public JSON Schema contracts into ``config/schemas/``."""

from __future__ import annotations

from pathlib import Path

from opendub.schemas.export import export_schemas


def main() -> None:
    destination = Path(__file__).resolve().parents[1] / "config" / "schemas"
    for filename in export_schemas(destination):
        print(destination / filename)


if __name__ == "__main__":
    main()
