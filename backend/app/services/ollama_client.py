import httpx
from fastapi import HTTPException, status

from app.core.config import get_settings


class OllamaClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = self.settings.ollama_base_url.rstrip("/")
        self.timeout = self.settings.ollama_timeout_seconds

    def health_check(self) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            response.raise_for_status()
        except httpx.HTTPError:
            return False
        return True

    def generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        body: dict = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3},
        }
        if json_mode:
            body["format"] = "json"

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=body,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Ollama generate request failed",
            ) from exc

        payload = response.json()
        return payload.get("response", "").strip()

    def embed(self, *, model: str, text: str) -> list[float]:
        errors: list[str] = []

        endpoints = [
            (
                "/api/embed",
                {"model": model, "input": text},
            ),
            (
                "/api/embeddings",
                {"model": model, "prompt": text},
            ),
        ]

        for path, payload in endpoints:
            try:
                response = httpx.post(
                    f"{self.base_url}{path}",
                    json=payload,
                    timeout=self.timeout,
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                errors.append(f"{path}: HTTP {exc.response.status_code}")
                continue
            except httpx.HTTPError as exc:
                errors.append(f"{path}: {exc.__class__.__name__}")
                continue

            data = response.json()
            embedding = data.get("embedding")
            if embedding is None and isinstance(data.get("embeddings"), list) and data["embeddings"]:
                embedding = data["embeddings"][0]

            if not isinstance(embedding, list):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Ollama returned an invalid embedding payload",
                )

            return [float(value) for value in embedding]

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Ollama embedding request failed. "
                f"Tried endpoints: {', '.join(errors)}. "
                f"Check OLLAMA_BASE_URL and ensure the embedding model '{model}' is installed."
            ),
        )
