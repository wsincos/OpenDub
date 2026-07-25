"""Safe redaction for event details exposed through logs and local APIs."""

from __future__ import annotations

from collections.abc import Mapping

_SENSITIVE_KEYS = frozenset(
    {"audio", "credential", "path", "prompt", "text", "token", "transcript"}
)


def redact_details(details: Mapping[str, object]) -> dict[str, object]:
    """Replace user content, filesystem paths, and credentials with a stable marker."""
    return {
        key: "[redacted]" if key.lower() in _SENSITIVE_KEYS else value
        for key, value in details.items()
    }
