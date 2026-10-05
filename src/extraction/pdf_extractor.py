# extractors/pdf_extractor.py
import pymupdf  # PyMuPDF (nom moderne, remplace "import fitz")
from pathlib import Path
from src.extraction.DocumentBase import Document


def extract_pdf(file_path: str) -> Document:
    """Extrait le texte d'un PDF avec métadonnées complètes."""
    path = Path(file_path)
    
    doc = pymupdf.open(file_path)
    
    try:
        # Extraction du texte page par page
        full_text = ""
        pages_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text("text")
            pages_text.append(page_text)
            
            full_text += f"\n\n--- PAGE {page_num + 1} ---\n\n{page_text}"
        
        # Métadonnées du PDF
        pdf_metadata = doc.metadata or {}
        
        return Document(
            text=full_text.strip(),
            source_filename=path.name,
            source_path=str(path.absolute()),
            file_format="pdf",
            file_size_bytes=path.stat().st_size,
            number_of_pages=len(doc),
            metadata={
                "pdf_title": pdf_metadata.get("title", ""),
                "pdf_author": pdf_metadata.get("author", ""),
                "pdf_subject": pdf_metadata.get("subject", ""),
                "pdf_creator": pdf_metadata.get("creator", ""),
                "pdf_producer": pdf_metadata.get("producer", ""),
                "pdf_creation_date": pdf_metadata.get("creationDate", ""),
                "pdf_modification_date": pdf_metadata.get("modDate", ""),
            }
        )
    
    finally:
        doc.close()