import wave

try:
    import boto3
except ImportError:
    boto3 = None  # type: ignore

from ...exceptions import ModuleNotInstalled
from ...tts import BaseTTS


class PollyTTS(BaseTTS):
    def __init__(self, client=None, voice_name=None, lang=None) -> None:
        if boto3 is None:
            raise ModuleNotInstalled("boto3")

        super().__init__(voice_name=voice_name or "Joanna", lang=lang)
        self.client = client

    def set_credentials(self, credentials) -> None:
        region, aws_key_id, aws_access_key = credentials
        if credentials:
            boto_session = boto3.Session(
                aws_access_key_id=aws_key_id,
                aws_secret_access_key=aws_access_key,
                region_name=region,
            )
        else:
            boto_session = boto3.Session()
        self.client = boto_session.client("polly")

    def synth(self, ssml: str, filename: str) -> None:
        resp = self.client.synthesize_speech(
            Engine="neural",
            OutputFormat="pcm",
            VoiceId=self.voice_name,
            TextType="ssml",
            Text=str(ssml),
        )

        with wave.open(filename, "wb") as wav:
            wav.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # type: ignore
            wav.writeframes(resp["AudioStream"].read())
