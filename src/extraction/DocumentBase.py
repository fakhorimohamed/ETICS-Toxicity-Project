# extractors/base.py
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
from datetime import datetime


@dataclass
class Document:
    """ Représentation standardisée d'un document extrait.
    """
    
    # Contenu
    text: str                          
    chunks: list[str] = field(default_factory=list) 
    
    # Métadonnées
    source_filename: str = ""          
    source_path: str = ""              
    file_format: str = ""              
    file_size_bytes: int = 0           
    number_of_pages: Optional[int] = None  
    extraction_date: str = ""          
    language: str = "unknown"         
    
    # Métadonnées spécifiques
    metadata: dict = field(default_factory=dict)  
    
    def __post_init__(self):
        if not self.extraction_date:
            self.extraction_date = datetime.now().strftime("%Y-%m-%d")
    
    @property
    def word_count(self) -> int:
        return len(self.text.split())
    
    @property
    def char_count(self) -> int:
        return len(self.text)



def extract_document(file_path: str) -> Document:
    """Fonction unifiée : dispatch vers le bon extracteur selon l'extension."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Le fichier n'existe pas : {file_path}")
    
    extension = path.suffix.lower()
    
    if extension == ".pdf":
        from src.extraction.pdf_extractor import extract_pdf
        return extract_pdf(file_path)
    elif extension == ".txt":
        from src.extraction.text_extractor import extract_txt
        return extract_txt(file_path)
    elif extension in [".docx", ".doc"]:
        if extension == ".doc":
            print("⚠️  Format .doc legacy détecté. Conversion recommandée en .docx.")
        from src.extraction.docx_extractor import extract_docx
        return extract_docx(file_path)
    else:
        raise ValueError(f"Format non supporté : {extension}. Formats acceptés : .pdf, .txt, .docx")