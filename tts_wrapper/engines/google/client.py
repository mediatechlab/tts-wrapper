from ...exceptions import ModuleNotInstalled

try:
    from google.cloud import texttospeech
    from google.oauth2 import service_account  # type: ignore
except ImportError:
    texttospeech = None  # type: ignore
    service_account = None  # type: ignore


class GoogleClient:
    def __init__(self, credentials: str) -> None:
        if texttospeech is None or service_account is None:
            raise ModuleNotInstalled("google-cloud-texttospeech")

        self.client = texttospeech.TextToSpeechClient(
            credentials=service_account.Credentials.from_service_account_file(
                credentials
            )
        )

    def synth(self, ssml: str, voice: str, lang: str, audio_config=None) -> bytes:
        s_input = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(language_code=lang, name=voice)
        audio_config = audio_config or texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        resp = self.client.synthesize_speech(
            input=s_input, voice=voice, audio_config=audio_config
        )
        return resp.audio_content
