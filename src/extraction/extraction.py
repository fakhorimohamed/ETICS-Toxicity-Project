import pymupdf
import re


def extraire_texte_propre(pdf_path):
    doc = pymupdf.open(pdf_path)
    texte = ""
    for page in doc:
        texte += page.get_text()
    
    # Nettoyage léger
    texte = re.sub(r'\n+', '\n', texte)         
    texte = re.sub(r'[ \t]+', ' ', texte)     
   
    texte = texte.strip()
    
    return texte

## texte_brut = extraire_texte_propre("contrat_de_travail_type.pdf")
## print(texte_brut)

if __name__ == "__main__":
    from pathlib import Path
    RACINE = Path(__file__).parent.parent.parent
    chemin = RACINE / "data" / "contrat_de_travail_type.pdf"
    print(extraire_texte_propre(str(chemin)))
