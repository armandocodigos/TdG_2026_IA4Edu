from abc import ABC, abstractmethod


class BaseLLMClient(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str
    ):

        pass