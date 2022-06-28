from abc import ABC, abstractmethod
from typing import Union

from . import AbstractSSMLNode

SSML = Union[str, AbstractSSMLNode]


class AbstractTTS(ABC):
    @abstractmethod
    def synth_to_bytes(self, ssml: SSML) -> bytes:
        pass

    def synth_to_file(self, ssml: SSML, filename: str) -> None:
        audio_content = self.synth_to_bytes(str(ssml))
        with open(filename, "wb") as wav:
            wav.write(audio_content)

    @abstractmethod
    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        pass
