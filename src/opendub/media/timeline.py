"""Subtitle ingestion with strict, microsecond-precise timeline invariants."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from opendub.domain.time import TimeRange

_TIMECODE_PATTERN = re.compile(
    r"^(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})[,.](?P<millis>\d{3})$"
)


@dataclass(frozen=True)
class SubtitleCue:
    """One imported subtitle line and its exact target time window."""

    range: TimeRange
    text: str


def import_srt(path: Path) -> tuple[SubtitleCue, ...]:
    """Import UTF-8 SubRip cues, rejecting malformed and overlapping time windows."""
    return _parse_cues(path.read_text(encoding="utf-8-sig"), is_vtt=False)


def import_vtt(path: Path) -> tuple[SubtitleCue, ...]:
    """Import UTF-8 WebVTT cues, rejecting malformed and overlapping time windows."""
    return _parse_cues(path.read_text(encoding="utf-8-sig"), is_vtt=True)


def _parse_cues(content: str, *, is_vtt: bool) -> tuple[SubtitleCue, ...]:
    normalized = content.replace("\r\n", "\n").replace("\r", "\n").strip()
    if is_vtt:
        if not normalized.startswith("WEBVTT"):
            raise ValueError("WebVTT file must start with WEBVTT")
        normalized = normalized.removeprefix("WEBVTT").lstrip(" \t\n")
    if not normalized:
        return ()

    cues: list[SubtitleCue] = []
    for block in re.split(r"\n[ \t]*\n", normalized):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        timing_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            raise ValueError("subtitle cue has no timing line")
        if timing_index == len(lines) - 1:
            raise ValueError("subtitle cue has no text")
        time_range = _parse_time_range(lines[timing_index])
        text = "\n".join(lines[timing_index + 1 :])
        cues.append(SubtitleCue(range=time_range, text=text))

    for previous, current in zip(cues, cues[1:], strict=False):
        if current.range.start_us < previous.range.end_us:
            raise ValueError("subtitle cues must not overlap")
    return tuple(cues)


def _parse_time_range(line: str) -> TimeRange:
    parts = [part.strip() for part in line.split("-->", maxsplit=1)]
    if len(parts) != 2:
        raise ValueError("subtitle timing line must contain -->")
    return TimeRange(
        start_us=_parse_timecode(parts[0]),
        end_us=_parse_timecode(parts[1].split()[0]),
    )


def _parse_timecode(value: str) -> int:
    match = _TIMECODE_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError(f"invalid subtitle timecode: {value}")
    hours = int(match["hours"])
    minutes = int(match["minutes"])
    seconds = int(match["seconds"])
    millis = int(match["millis"])
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"invalid subtitle timecode: {value}")
    return (((hours * 60 + minutes) * 60 + seconds) * 1_000 + millis) * 1_000
