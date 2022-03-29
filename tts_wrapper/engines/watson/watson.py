from ...exceptions import ModuleNotInstalled
from ...tts import BaseTTS

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import TextToSpeechV1
except:
    IAMAuthenticator = None
    TextToSpeechV1 = None


class WatsonTTS(BaseTTS):
    def __init__(self, client=None, voice_name=None, lang=None) -> None:
        if IAMAuthenticator is None or TextToSpeechV1 is None:
            raise ModuleNotInstalled("ibm-watson")
        super().__init__(voice_name=voice_name or "en-US_LisaV3Voice", lang=lang)
        self.client = client

    def set_credentials(self, credentials) -> None:
        api_key, api_url = credentials
        client = TextToSpeechV1(authenticator=IAMAuthenticator(api_key))
        client.set_service_url(api_url)
        self.client = client

    def synth(self, ssml: str, filename: str) -> None:
        resp = self.client.synthesize(
            text=str(ssml), voice=self.voice_name, accept="audio/wav"
        )
        with open(filename, "wb") as wav:
            content = resp.get_result().content

            wav.write(content)
