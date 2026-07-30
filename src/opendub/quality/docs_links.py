"""Validate local Markdown file links without following external URLs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
_SKIPPED_DIRECTORIES = frozenset({".git", ".venv", "archive", "node_modules"})


@dataclass(frozen=True)
class InvalidMarkdownLink:
    """A Markdown link whose local target is missing or escapes the repository."""

    source: Path
    target: str


def find_invalid_local_markdown_links(root: Path) -> tuple[InvalidMarkdownLink, ...]:
    """Return sorted invalid local Markdown links rooted at ``root``.

    External URLs, anchor-only targets, and inline-code examples are intentionally skipped.
    """
    resolved_root = root.resolve()
    invalid: list[InvalidMarkdownLink] = []
    for source in _markdown_files(resolved_root):
        for target in _local_targets(source):
            candidate = (source.parent / unquote(target)).resolve()
            if not candidate.is_relative_to(resolved_root) or not candidate.exists():
                invalid.append(InvalidMarkdownLink(source=source, target=target))
    return tuple(sorted(invalid, key=lambda item: (str(item.source), item.target)))


def _markdown_files(root: Path) -> tuple[Path, ...]:
    return tuple(
        path
        for path in sorted(root.rglob("*.md"))
        if not _SKIPPED_DIRECTORIES.intersection(path.relative_to(root).parts)
    )


def _local_targets(source: Path) -> tuple[str, ...]:
    targets: list[str] = []
    in_fenced_block = False
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fenced_block = not in_fenced_block
            continue
        if in_fenced_block:
            continue
        for match in _LINK_PATTERN.finditer(line):
            target = (match.group(1) or match.group(2)).split("#", maxsplit=1)[0]
            if target and not _is_external_target(target):
                targets.append(target)
    return tuple(targets)


def _is_external_target(target: str) -> bool:
    return target.startswith(("https://", "http://", "mailto:", "tel:", "data:"))
