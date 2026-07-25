"""Explicit state transitions for editable dubbing segments."""

from __future__ import annotations

from opendub.domain.segments import DubbingSegment, SegmentStatus

_ALLOWED_TRANSITIONS: dict[SegmentStatus, frozenset[SegmentStatus]] = {
    "unconfigured": frozenset({"ready"}),
    "ready": frozenset({"synthesizing"}),
    "synthesizing": frozenset({"generated", "failed", "cancelled"}),
    "generated": frozenset({"ready", "accepted", "synthesizing"}),
    "accepted": frozenset({"ready", "synthesizing"}),
    "failed": frozenset({"ready", "synthesizing"}),
    "cancelled": frozenset({"ready", "synthesizing"}),
}


def transition_segment(segment: DubbingSegment, target: SegmentStatus) -> DubbingSegment:
    """Return a revised segment if the state transition is valid."""
    if target not in _ALLOWED_TRANSITIONS[segment.status]:
        raise ValueError(f"cannot transition segment from {segment.status} to {target}")
    return segment.model_copy(update={"status": target, "revision": segment.revision + 1})
