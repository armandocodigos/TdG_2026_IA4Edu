import ollama

from core.tutoring.llm.base_client import (
    BaseLLMClient
)


class OllamaClient(
    BaseLLMClient
):

    def __init__(
        self,
        model: str
    ):

        self.model = model

    def generate(
        self,
        prompt: str
    ):

        response = ollama.chat(

            model=self.model,

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ]
        )

        return (
            response["message"]["content"]
        )
