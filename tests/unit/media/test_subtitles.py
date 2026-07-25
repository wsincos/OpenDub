from pathlib import Path

import pytest

from opendub.media.timeline import import_srt, import_vtt


def test_import_srt_preserves_unicode_text_and_microsecond_timing(tmp_path: Path) -> None:
    subtitle = tmp_path / "dialogue.srt"
    subtitle.write_text(
        "1\n00:00:00,100 --> 00:00:01,250\n你好，OpenDub。\n\n"
        "2\n00:00:01,250 --> 00:00:02,000\nEmotion follows the picture.\n",
        encoding="utf-8",
    )

    cues = import_srt(subtitle)

    assert cues[0].range.start_us == 100_000
    assert cues[0].range.end_us == 1_250_000
    assert cues[0].text == "你好，OpenDub。"


@pytest.mark.parametrize(
    "content",
    [
        "1\n00:00:01,000 --> 00:00:01,000\nZero length\n",
        "1\nnot-a-time --> 00:00:01,000\nInvalid\n",
        "1\n00:00:00,000 --> 00:00:02,000\nFirst\n\n2\n00:00:01,000 --> 00:00:03,000\nOverlap\n",
    ],
)
def test_import_srt_rejects_invalid_or_overlapping_cues(tmp_path: Path, content: str) -> None:
    subtitle = tmp_path / "invalid.srt"
    subtitle.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        import_srt(subtitle)


def test_import_vtt_reads_cues(tmp_path: Path) -> None:
    subtitle = tmp_path / "dialogue.vtt"
    subtitle.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:00.500\nOpening line\n", encoding="utf-8")

    cues = import_vtt(subtitle)

    assert len(cues) == 1
    assert cues[0].range.duration_us == 500_000
