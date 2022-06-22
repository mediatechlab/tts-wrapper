from abc import ABC, abstractmethod

from . import AbstractSSMLNode, SSMLNode


class AbstractTTS(ABC):
    @abstractmethod
    def synth(self, ssml: str, filename: str) -> None:
        pass

    @abstractmethod
    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        pass

    @abstractmethod
    def set_credentials(self, credentials) -> None:
        pass

    @abstractmethod
    def set_voice(self, voice_name: str, lang: str) -> None:
        pass


class BaseTTS(AbstractTTS):
    def __init__(self, voice_name=None, lang=None) -> None:
        self.voice_name = voice_name
        self.lang = lang or "en-US"

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)

    def set_voice(self, voice_name: str, lang: str = None) -> None:
        self.voice_name = voice_name
        self.lang = lang
