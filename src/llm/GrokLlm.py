from groq import Groq
from src.configs import settings
import json


class GroqClient:
    """Client Groq pour l'évaluation de toxicité éthique."""
    
    def __init__(self, model: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY manquante dans .env")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = model or settings.toxicity_model
    
    def generate_json(self, prompt: str, temperature: float = None) -> dict:
        temp = temperature if temperature is not None else settings.temperature_toxicity
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Tu réponds UNIQUEMENT en JSON valide, sans texte avant ou après."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=temp,
            max_tokens=4096,
        )
        
        return json.loads(response.choices[0].message.content)


groq_toxicity = GroqClient(model=settings.toxicity_model)