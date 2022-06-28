from typing import Optional

import requests

from ...exceptions import ModuleNotInstalled

try:
    import requests
except ImportError:
    requests = None  # type: ignore


class MicrosoftClient:
    def __init__(
        self, credentials: str, region: Optional[str] = None, verify_ssl=True
    ) -> None:
        if requests is None:
            raise ModuleNotInstalled("requests")

        self.credentials = credentials
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.region = region or "eastus"

    def _fetch_access_token(self) -> str:
        fetch_token_url = (
            f"https://{self.region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        headers = {"Ocp-Apim-Subscription-Key": self.credentials}
        response = requests.post(fetch_token_url, headers=headers)
        return str(response.text)

    def synth(self, ssml: str) -> bytes:
        if "Authorization" not in self.session.headers:
            access_token = self._fetch_access_token()
            self.session.headers.update(
                {
                    "Authorization": "Bearer " + access_token,
                    "Content-Type": "application/ssml+xml",
                    "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
                }
            )

        response = self.session.post(
            f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1",
            data=ssml.encode("utf-8"),
        )

        if response.status_code != 200:
            raise Exception(f"Server replied with {response.status_code}")

        return response.content
