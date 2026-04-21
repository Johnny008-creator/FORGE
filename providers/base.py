from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def detect(self) -> str:
        """Detect if the provider is available and return base URL/config."""
        pass

    @abstractmethod
    def get_models(self) -> list:
        """Return list of available models."""
        pass

    @abstractmethod
    def stream_chat(self, messages: list, model: str, profile: dict) -> tuple:
        """Stream chat response and return (text, stats)."""
        pass
