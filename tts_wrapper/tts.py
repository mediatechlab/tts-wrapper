from abc import ABC, abstractmethod
from typing import Any, List, Literal, Optional, Union

FileFormat = Union[Literal["wav"], Literal["mp3"]]


class AbstractTTS(ABC):
    @classmethod
    @abstractmethod
    def supported_formats(cls) -> List[FileFormat]:
        pass

    @abstractmethod
    def synth_to_bytes(self, text: Any, format: FileFormat) -> bytes:
        pass

    def synth_to_file(
        self, text: Any, filename: str, format: Optional[FileFormat] = None
    ) -> None:
        audio_content = self.synth_to_bytes(text, format=format or "wav")
        with open(filename, "wb") as wav:
            wav.write(audio_content)
