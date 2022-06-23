from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

from ...exceptions import ModuleNotInstalled
from ...tts import SSML, AbstractTTS

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import TextToSpeechV1
except ImportError:
    IAMAuthenticator = None
    TextToSpeechV1 = None

Credentials = tuple[str, str]


class WatsonTTS(AbstractTTS):
    def __init__(self, credentials: Credentials, voice=None, lang=None) -> None:
        if IAMAuthenticator is None or TextToSpeechV1 is None:
            raise ModuleNotInstalled("ibm-watson")

        self.voice = (voice or "en-US_LisaV3Voice",)
        self.lang = lang or "en-US"

        api_key, api_url = credentials
        client = TextToSpeechV1(authenticator=IAMAuthenticator(api_key))
        client.set_service_url(api_url)
        self.client = client

    def synth(self, ssml: SSML, filename: str) -> None:
        resp = self.client.synthesize(
            text=str(ssml), voice=self.voice, accept="audio/wav"
        )
        with open(filename, "wb") as wav:
            content = resp.get_result().content

            wav.write(content)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
