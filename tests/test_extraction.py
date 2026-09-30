from pathlib import Path

import fitz
import pytest

from src.extraction.pdf_reader import read_pdf


def _write_pdf(path: Path, pages: list[str]) -> None:
    document = fitz.open()
    for text in pages:
        page = document.new_page()
        page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def test_read_pdf_concatenates_pages(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    _write_pdf(pdf_path, ["First page text", "Second page text"])

    text = read_pdf(str(pdf_path))

    assert "First page text" in text
    assert "Second page text" in text
    assert text.index("First page text") < text.index("Second page text")


def test_read_pdf_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_pdf(str(tmp_path / "missing.pdf"))


def test_read_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    other = tmp_path / "notes.txt"
    other.write_text("not a pdf", encoding="utf-8")

    with pytest.raises(ValueError):
        read_pdf(str(other))
