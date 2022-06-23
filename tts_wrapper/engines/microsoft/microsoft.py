from typing import Optional

from ...exceptions import ModuleNotInstalled
from ...ssml import AbstractSSMLNode, SSMLNode
from ...tts import SSML, AbstractTTS

try:
    import requests
except ImportError:
    requests = None  # type: ignore


class MicrosoftTTS(AbstractTTS):
    def __init__(
        self, credentials: str, lang=None, voice=None, region=None, verify_ssl=True
    ) -> None:
        if requests is None:
            raise ModuleNotInstalled("requests")

        self.credentials = credentials
        self.lang = lang or "en-US"
        self.voice = voice or "en-US-JessaNeural"
        self.region = region or "eastus"
        self.access_token: Optional[str] = None
        self.sess = requests.Session()
        self.sess.verify = verify_ssl

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak(
            {
                "version": "1.0",
                "xml:lang": self.lang,
                "xmlns": "https://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
            }
        ).add(SSMLNode.voice({"name": self.voice}).add(ssml))

    def synth(self, ssml: SSML, filename: str) -> None:
        self.access_token = self.access_token or self._fetch_access_token()

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        }

        response = self.sess.post(
            f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1",
            headers=headers,
            data=str(ssml).encode("utf-8"),
        )

        if response.status_code != 200:
            raise Exception(f"Server replied with {response.status_code}")

        assert response.content

        with open(filename, "wb") as wav:
            wav.write(response.content)

    def _fetch_access_token(self) -> str:
        fetch_token_url = (
            f"https://{self.region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        headers = {"Ocp-Apim-Subscription-Key": self.credentials}
        response = self.sess.post(fetch_token_url, headers=headers)
        return str(response.text)
