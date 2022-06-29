from typing import Optional

from tts_wrapper.exceptions import UnsupportedFileFormat
from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

from ...tts import SSML, AbstractTTS, FileFormat
from . import WatsonClient


class WatsonTTS(AbstractTTS):
    def __init__(
        self,
        client: WatsonClient,
        voice: Optional[str] = None,
    ) -> None:
        self.client = client
        self.voice = voice or "en-US_LisaV3Voice"

    def synth_to_bytes(self, ssml: SSML, format: FileFormat) -> bytes:
        if format not in ("wav", "mp3"):
            raise UnsupportedFileFormat(format, self.__class__.__name__)
        return self.client.synth(str(ssml), voice=self.voice, format=format)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
