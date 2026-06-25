from app.core.config import get_settings
from app.services.ollama_client import OllamaClient


class EmbeddingService:
    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        self.settings = get_settings()
        self.ollama_client = ollama_client or OllamaClient()

    def embed_text(self, text: str) -> list[float]:
        return self.ollama_client.embed(model=self.settings.embedding_model, text=text)
