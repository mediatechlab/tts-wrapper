from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode
from ...exceptions import ModuleNotInstalled
from ...tts import SSML, AbstractTTS

try:
    from google.cloud import texttospeech
    from google.oauth2 import service_account
except ImportError:
    texttospeech = None  # type: ignore
    service_account = None  # type: ignore


class GoogleTTS(AbstractTTS):
    def __init__(self, credentials: str, lang=None, voice=None) -> None:
        """
        @param credentials: The path to the json file that contains the credentials.
        """
        if texttospeech is None or service_account is None:
            raise ModuleNotInstalled("google-cloud-texttospeech")

        self.client = self._setup_client(credentials)
        self.lang = lang or "en-US"
        self.voice = voice or "en-US-Wavenet-C"

    def _setup_client(self, credentials: str) -> texttospeech.TextToSpeechClient:
        return texttospeech.TextToSpeechClient(
            credentials=service_account.Credentials.from_service_account_file(
                credentials
            )
        )

    def synth(self, ssml: SSML, filename: str) -> None:
        s_input = texttospeech.SynthesisInput(ssml=str(ssml))

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang, name=self.voice
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        resp = self.client.synthesize_speech(
            input=s_input, voice=voice, audio_config=audio_config
        )

        assert resp.audio_content

        with open(filename, "wb") as f:
            f.write(resp.audio_content)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
