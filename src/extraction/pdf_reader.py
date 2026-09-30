from pathlib import Path

import fitz

from src.utils.logger import logger


def read_pdf(path: str) -> str:
    """Extract text from a PDF, keeping pages in order.

    Returns concatenated page text. Pages with no extractable text are skipped.
    Raises FileNotFoundError if the path does not exist, and ValueError if it
    is not a PDF.
    """
    pdf_path = Path(path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path.name}")

    pages: list[str] = []
    with fitz.open(pdf_path) as document:
        for page in document:
            text = page.get_text("text", sort=True).strip()
            if text:
                pages.append(text)

    if not pages:
        logger.warning("No extractable text in %s (empty or scanned PDF)", pdf_path)

    return "\n\n".join(pages)
