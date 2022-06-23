from abc import ABC, abstractmethod
from typing import Union

from . import AbstractSSMLNode

SSML = Union[str, AbstractSSMLNode]


class AbstractTTS(ABC):
    @abstractmethod
    def synth(self, ssml: SSML, filename: str) -> None:
        pass

    @abstractmethod
    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        pass
