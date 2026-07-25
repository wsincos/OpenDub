"""Cooperative cancellation token shared between pipelines and model runtimes."""

from __future__ import annotations

from threading import Event


class CancellationToken:
    """A thread-safe one-way cancellation signal."""

    def __init__(self) -> None:
        self._event = Event()

    def cancel(self) -> None:
        """Request cancellation of in-flight cooperative work."""
        self._event.set()

    @property
    def cancelled(self) -> bool:
        """Return whether cancellation was requested."""
        return self._event.is_set()
