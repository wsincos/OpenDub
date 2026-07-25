from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess

from opendub.media.audio import normalize_reference_audio
from opendub.media.ffmpeg import FfmpegRunner
from opendub.media.probe import parse_probe_output
from opendub.media.render import mux_video


def test_ffmpeg_runner_keeps_hostile_filename_as_one_argument(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    captured: dict[str, object] = {}

    def fake_run(*args: object, **kwargs: object) -> CompletedProcess[str]:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return CompletedProcess(args[0], 0, stdout="ok", stderr="")

    monkeypatch.setattr("opendub.media.ffmpeg.subprocess.run", fake_run)
    source = Path("input; not-a-command 视频 file.mp4")

    FfmpegRunner().run(("-i", str(source), "output.mp4"))

    command = captured["args"][0]
    assert command == ["ffmpeg", "-i", str(source), "output.mp4"]
    assert captured["kwargs"]["shell"] is False


def test_normalize_reference_audio_builds_mono_pcm_wav_command(monkeypatch, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    captured: list[tuple[str, ...]] = []

    class FakeRunner:
        def run(self, arguments: tuple[str, ...]) -> None:
            captured.append(arguments)

    destination = tmp_path / "normalized.wav"
    normalize_reference_audio(
        Path("speaker; source.wav"),
        destination,
        runner=FakeRunner(),  # type: ignore[arg-type]
    )

    assert captured == [
        (
            "-y",
            "-i",
            "speaker; source.wav",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "24000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        )
    ]


def test_parse_probe_output_reads_machine_json() -> None:
    probe = parse_probe_output(
        '{"format":{"duration":"1.25","format_name":"mov,mp4,m4a"},'
        '"streams":[{"codec_type":"video","width":1920,"height":1080},'
        '{"codec_type":"audio","sample_rate":"48000","channels":2}]}'
    )

    assert probe.duration_us == 1_250_000
    assert probe.video_width == 1920
    assert probe.audio_sample_rate == 48_000


def test_mux_video_marks_ai_generated_dubbing_for_every_audio_policy(tmp_path: Path) -> None:
    captured: list[tuple[str, ...]] = []

    class FakeRunner:
        def run(self, arguments: tuple[str, ...]) -> None:
            captured.append(arguments)

    for mode in ("remove", "preserve", "duck"):
        mux_video(
            Path("source.mp4"),
            Path("dubbing.wav"),
            tmp_path / f"{mode}.mp4",
            mode=mode,
            runner=FakeRunner(),  # type: ignore[arg-type]
        )

    assert len(captured) == 3
    for command in captured:
        metadata_index = command.index("-metadata")
        assert command[metadata_index + 1] == "comment=AI-generated dubbing by OpenDub"
