# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Configuration centralisée du projet ETICS - Toxicité des contrats."""
    

    # API KEYs 
    GEMINI_API_KEY: str = Field(..., description="Clé API Google Gemini")
    GROQ_API_KEY: Optional[str] = Field(None, description="Clé API Groq")
    
    # CHUNKING 
    
    chunk_size: int = Field(default=1500,ge=100,le=10000,description="Taille optimale pour les contrats de travail (une clause = 500-1500 chars)")
    
    chunk_overlap: int = Field(default=100,ge=0,le=1000,description="Overlap minimal pour éviter les coupures sans dupliquer excessivement")
    
    # LLMs

    # Gemini pour l'extraction structurée
    extraction_model: str = Field(default="gemini-2.5-flash",description="Modèle pour l'extraction structurée (JSON)")
    temperature_extraction: float = Field(default=0.1,ge=0.0,le=2.0,description="Température basse pour extraction déterministe")
    
    # Groq pour la toxicité
    toxicity_model: str = Field(default="llama-3.3-70b-versatile",description="Modèle pour l'évaluation éthique (raisonnement complexe)")
    temperature_toxicity: float = Field(default=0.2,ge=0.0,le=2.0,description="Température légèrement plus haute pour nuance éthique")
    

    # PATHs 

    output_folder: str = Field(default="./results",description="Dossier de sortie des résultats JSON")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="",
    )
    
    def validate_api_keys(self) -> None:
        """Vérifie qu'au moins une clé API LLM est présente."""
        if not self.GEMINI_API_KEY and not self.GROQ_API_KEY:
            raise ValueError(
                "Au moins une clé API LLM doit être définie dans .env "
                "(GEMINI_API_KEY ou GROQ_API_KEY)"
            )
    
    def get_active_llm_providers(self) -> list[str]:
        """Retourne la liste des fournisseurs LLM actifs."""
        providers = []
        if self.GEMINI_API_KEY:
            providers.append("gemini")
        if self.GROQ_API_KEY:
            providers.append("groq")
        return providers


settings = Settings()
settings.validate_api_keys()