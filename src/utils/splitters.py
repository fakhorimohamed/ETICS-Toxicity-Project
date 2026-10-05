# src/extraction/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.extraction.DocumentBase import Document


CONTRACT_SEPARATORS = [
    "\n\n--- PAGE",       
    "\n\n--- TABLEAU",    
    "\n\nArticle",        
    "\n\nClause",         
    "\n\nChapitre",       
    "\n\nSection",       
    "\n\n",               
    "\n",                 
    ". ",               
    "! ",                 
    "? ",                 
    "; ",                 
    ", ",                 
    " ",                  
    "",                  
]


def split_document(
    doc: Document,
    chunk_size: int = 1500,
    chunk_overlap: int = 100,
) -> Document:
    """
    Découpe un Document en chunks optimisés pour les contrats de travail.
    
    Args:
        doc: Le Document à découper (doit avoir doc.text rempli)
        chunk_size: Taille max de chaque chunk en caractères
        chunk_overlap: Nombre de caractères de chevauchement entre chunks
    
    Returns:
        Le même Document avec doc.chunks rempli
    """
    if not doc.text or len(doc.text.strip()) == 0:
        print(f" Document vide : {doc.source_filename}")
        doc.chunks = []
        return doc
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=CONTRACT_SEPARATORS,
        length_function=len,
        keep_separator=False,
    )
    
    doc.chunks = splitter.split_text(doc.text)
    
    print(f"{doc.source_filename} → {len(doc.chunks)} chunks "
          f"(size={chunk_size}, overlap={chunk_overlap})")
    
    return doc