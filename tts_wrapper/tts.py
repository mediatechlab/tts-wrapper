from abc import ABC, abstractmethod
from typing import Literal, Optional, Union

from . import AbstractSSMLNode

SSML = Union[str, AbstractSSMLNode]
FileFormat = Union[Literal["wav"], Literal["mp3"]]


class AbstractTTS(ABC):
    @abstractmethod
    def synth_to_bytes(self, ssml: SSML, format: FileFormat) -> bytes:
        pass

    def synth_to_file(
        self, ssml: SSML, filename: str, format: Optional[FileFormat] = None
    ) -> None:
        audio_content = self.synth_to_bytes(str(ssml), format=format or "wav")
        with open(filename, "wb") as wav:
            wav.write(audio_content)

    @abstractmethod
    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        pass
