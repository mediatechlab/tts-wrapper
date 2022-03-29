from ...exceptions import ModuleNotInstalled
from ...ssml import SSMLNode
from ...tts import BaseTTS

try:
    import requests
except ImportError:
    requests = None


class MicrosoftTTS(BaseTTS):
    def __init__(
        self, lang=None, voice_name=None, region=None, credentials=None, verify_ssl=True
    ) -> None:
        if requests is None:
            raise ModuleNotInstalled("requests")

        super().__init__(voice_name=voice_name or "en-US-JessaNeural", lang=lang)
        self.region = region or "eastus"
        self.credentials = credentials
        self.access_token = None
        self.sess = requests.Session()
        self.sess.verify = verify_ssl

    def create_ssml_root(self) -> SSMLNode:
        return SSMLNode.speak(
            {
                "version": "1.0",
                "xml:lang": self.lang,
                "xmlns": "https://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
            }
        ).add(SSMLNode.voice({"name": self.voice_name}))

    def set_credentials(self, credentials: str) -> None:
        self.credentials = credentials

    def synth(self, ssml: str, filename: str) -> None:
        if not self.access_token:
            self.access_token = self._fetch_access_token()

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

    def _fetch_access_token(self):
        fetch_token_url = (
            f"https://{self.region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        headers = {"Ocp-Apim-Subscription-Key": self.credentials}
        response = self.sess.post(fetch_token_url, headers=headers)
        return str(response.text)
