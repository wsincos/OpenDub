"""Canonical cache keys that make model, input, and seed changes observable."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping


def stage_cache_key(values: Mapping[str, object]) -> str:
    """Hash a canonical stage input mapping without omitting any declared input."""
    encoded = json.dumps(
        values,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
