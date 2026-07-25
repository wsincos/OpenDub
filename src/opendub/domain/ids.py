"""UUIDv7 identifiers used by every persistent OpenDub domain object."""

from __future__ import annotations

import uuid

from uuid6 import uuid7


def new_id() -> str:
    """Create a time-sortable UUIDv7 string."""
    return str(uuid7())


def validate_uuid7(value: str) -> str:
    """Return a canonical UUIDv7 string or raise ``ValueError``."""
    try:
        parsed = uuid.UUID(value)
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("must be a canonical UUIDv7 string") from error
    if parsed.version != 7 or str(parsed) != value:
        raise ValueError("must be a canonical UUIDv7 string")
    return value
