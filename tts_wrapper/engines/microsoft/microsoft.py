from typing import List, Optional

from tts_wrapper.exceptions import UnsupportedFileFormat

from ...ssml import AbstractSSMLNode, SSMLNode
from ...tts import SSML, AbstractTTS, FileFormat
from . import MicrosoftClient


class MicrosoftTTS(AbstractTTS):
    @classmethod
    def supported_formats(cls) -> List[FileFormat]:
        return ["wav", "mp3"]

    def __init__(
        self,
        client: MicrosoftClient,
        lang: Optional[str] = None,
        voice: Optional[str] = None,
    ) -> None:
        self.client = client
        self.lang = lang or "en-US"
        self.voice = voice or "en-US-JessaNeural"

    def synth_to_bytes(self, ssml: SSML, format: FileFormat) -> bytes:
        if format not in self.supported_formats():
            raise UnsupportedFileFormat(format, self.__class__.__name__)
        return self.client.synth(str(ssml), format)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak(
            {
                "version": "1.0",
                "xml:lang": self.lang,
                "xmlns": "https://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
            }
        ).add(SSMLNode.voice({"name": self.voice}).add(ssml))
