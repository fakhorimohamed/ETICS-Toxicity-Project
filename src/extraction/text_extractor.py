# extractors/txt_extractor.py
from pathlib import Path
from charset_normalizer import from_path
from src.extraction.DocumentBase import Document


def extract_txt(file_path: str) -> Document:
    """Extrait le texte d'un fichier TXT avec détection automatique d'encodage."""
    path = Path(file_path)
    
    # Détection automatique de l'encodage (UTF-8, Latin-1, Windows-1252...)
    result = from_path(file_path).best()
    
    if result is None:
        raise ValueError(f"Impossible de détecter l'encodage du fichier : {file_path}")
    
    encoding = result.encoding
    text = str(result)
    
    return Document(
        text=text.strip(),
        source_filename=path.name,
        source_path=str(path.absolute()),
        file_format="txt",
        file_size_bytes=path.stat().st_size,
        number_of_pages=None,  # Pas de notion de page pour TXT
        metadata={
            "detected_encoding": encoding,
            "detected_language": result.language if hasattr(result, 'language') else "unknown",
        }
    )