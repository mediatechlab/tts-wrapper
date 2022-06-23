import wave
from typing import Optional

from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

try:
    import boto3
except ImportError:
    boto3 = None  # type: ignore

from ...exceptions import ModuleNotInstalled
from ...tts import SSML, AbstractTTS

Credentials = tuple[str, str, str]


class PollyTTS(AbstractTTS):
    def __init__(
        self, credentials: Optional[Credentials] = None, voice=None, lang=None
    ) -> None:
        if boto3 is None:
            raise ModuleNotInstalled("boto3")

        self.voice = voice or "Joanna"
        self.lang = lang or "en-US"

        if credentials is None:
            boto_session = boto3.Session()
        else:
            region, aws_key_id, aws_access_key = credentials
            boto_session = boto3.Session(
                aws_access_key_id=aws_key_id,
                aws_secret_access_key=aws_access_key,
                region_name=region,
            )
        self.client = boto_session.client("polly")

    def synth(self, ssml: SSML, filename: str) -> None:
        resp = self.client.synthesize_speech(
            Engine="neural",
            OutputFormat="pcm",
            VoiceId=self.voice,
            TextType="ssml",
            Text=str(ssml),
        )

        with wave.open(filename, "wb") as wav:
            wav.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # type: ignore
            wav.writeframes(resp["AudioStream"].read())

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
