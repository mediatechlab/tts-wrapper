from typing import Optional

from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

from ...tts import SSML, AbstractTTS
from . import GoogleClient


class GoogleTTS(AbstractTTS):
    def __init__(
        self,
        client: GoogleClient,
        lang: Optional[str] = None,
        voice: Optional[str] = None,
    ) -> None:
        """
        @param credentials: The path to the json file that contains the credentials.
        """
        self.client = client
        self.lang = lang or "en-US"
        self.voice = voice or "en-US-Wavenet-C"

    def synth_to_bytes(self, ssml: SSML) -> bytes:
        return self.client.synth(str(ssml), self.voice, self.lang)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
