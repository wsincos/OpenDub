from pathlib import Path

from opendub.quality.docs_links import find_invalid_local_markdown_links


def test_docs_link_checker_ignores_external_links_and_accepts_existing_relative_files(
    tmp_path: Path,
) -> None:
    (tmp_path / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "[Guide](guide.md#section) [Website](https://example.test/docs)\n",
        encoding="utf-8",
    )

    assert find_invalid_local_markdown_links(tmp_path) == ()


def test_docs_link_checker_accepts_existing_relative_directories(tmp_path: Path) -> None:
    (tmp_path / "guides").mkdir()
    (tmp_path / "README.md").write_text("[Guides](guides/)\n", encoding="utf-8")

    assert find_invalid_local_markdown_links(tmp_path) == ()


def test_docs_link_checker_ignores_private_archives(tmp_path: Path) -> None:
    archive = tmp_path / "archive" / "private"
    archive.mkdir(parents=True)
    (archive / "historical-plan.md").write_text("[Old link](removed.md)\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("[Public docs](docs/)\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()

    assert find_invalid_local_markdown_links(tmp_path) == ()


def test_docs_link_checker_reports_missing_or_escaping_relative_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "[Missing](missing.md) [Escaping](../outside.md)\n",
        encoding="utf-8",
    )

    invalid = find_invalid_local_markdown_links(tmp_path)

    assert [item.target for item in invalid] == ["../outside.md", "missing.md"]
