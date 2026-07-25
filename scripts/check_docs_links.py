"""Fail when repository Markdown has broken local file links."""

from __future__ import annotations

from pathlib import Path

from opendub.quality.docs_links import find_invalid_local_markdown_links


def main() -> int:
    """Check repository documentation and emit concise, relocatable diagnostics."""
    root = Path(__file__).resolve().parents[1]
    invalid = find_invalid_local_markdown_links(root)
    for item in invalid:
        print(f"{item.source.relative_to(root)}: {item.target}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
