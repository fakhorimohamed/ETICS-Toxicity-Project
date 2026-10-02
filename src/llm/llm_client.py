from src.configs.Settings import settings 
class LLMClient:
    def complete(self, prompt: str) -> str:
        raise NotImplementedError

