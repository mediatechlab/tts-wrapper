import wave
from io import BytesIO
from typing import Optional, Tuple

from ...exceptions import ModuleNotInstalled

try:
    import boto3
except ImportError:
    boto3 = None  # type: ignore


Credentials = Tuple[str, str, str]


class PollyClient:
    def __init__(
        self,
        credentials: Optional[Credentials] = None,
    ) -> None:
        if boto3 is None:
            raise ModuleNotInstalled("boto3")

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

    def synth(self, ssml: str, voice: str) -> bytes:
        pcm = self.client.synthesize_speech(
            Engine="neural",
            OutputFormat="pcm",
            VoiceId=voice,
            TextType="ssml",
            Text=ssml,
        )["AudioStream"].read()

        bio = BytesIO()
        with wave.open(bio, "wb") as wav:
            wav.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # type: ignore
            wav.writeframes(pcm)

        return bio.getbuffer()
