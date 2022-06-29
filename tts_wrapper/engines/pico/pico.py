from typing import List, Optional

from tts_wrapper.exceptions import UnsupportedFileFormat
from tts_wrapper.ssml import AbstractSSMLNode

from ...tts import SSML, AbstractTTS, FileFormat
from . import PicoClient


class PicoTTS(AbstractTTS):
    @classmethod
    def supported_formats(cls) -> List[FileFormat]:
        return ["wav"]

    def __init__(self, client: PicoClient, voice: Optional[str] = None) -> None:
        self.client = client
        self.voice = voice or "en-US"

    def synth_to_bytes(self, ssml: SSML, format: FileFormat) -> bytes:
        if format not in self.supported_formats():
            raise UnsupportedFileFormat(format, self.__class__.__name__)

        return self.client.synth(str(ssml), self.voice)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return ssml
