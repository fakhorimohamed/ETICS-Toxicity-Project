# llm/gemini_client.py
from google import genai
from google.genai import types
from src.configs import settings
import json


class GeminiClient:
    """Client pour l'API Google Gemini."""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = model
    
    def generate_json(self, prompt: str, temperature: float = settings.temperature_extraction) -> dict:
        """Génère une réponse JSON structurée."""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",  # Force le mode JSON
            )
        )
        
        return json.loads(response.text)
    
    def generate_text(self, prompt: str, temperature: float = 0.2) -> str:
        """Génère une réponse texte libre."""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
            )
        )
        
        return response.text


# Instances pré-configurées
gemini_flash = GeminiClient(model=settings.extraction_model) 