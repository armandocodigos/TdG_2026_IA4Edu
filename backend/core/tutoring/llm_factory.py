from core.tutoring.llm.ollama_client import (
    OllamaClient
)


def build_llm(
    model_name: str
):

    return OllamaClient(
        model=model_name
    )
