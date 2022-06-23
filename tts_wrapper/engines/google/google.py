from ...exceptions import ModuleNotInstalled
from ...tts import BaseTTS

try:
    from google.cloud import texttospeech
    from google.oauth2 import service_account
except ImportError:
    texttospeech = None  # type: ignore
    service_account = None  # type: ignore


class GoogleTTS(BaseTTS):
    def __init__(self, client=None, lang=None, voice_name=None) -> None:
        if texttospeech is None or service_account is None:
            raise ModuleNotInstalled("google-cloud-texttospeech")

        super().__init__(lang=lang, voice_name=voice_name or "en-US-Wavenet-C")
        self.client = client

    def set_credentials(self, credentials: str) -> None:
        """
        @param credentials: The path to the json file that contains the credentials.
        """
        self.client = texttospeech.TextToSpeechClient(
            credentials=service_account.Credentials.from_service_account_file(
                credentials
            )
        )

    def synth(self, ssml: str, filename: str) -> None:
        s_input = texttospeech.SynthesisInput(ssml=str(ssml))

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang, name=self.voice_name
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
