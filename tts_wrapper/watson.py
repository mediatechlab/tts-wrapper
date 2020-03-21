from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1

from .tts import TTS


class WatsonTTS(TTS):
    def __init__(self, api_key, api_url, voice_name=None, lang=None) -> None:
        super().__init__(voice_name=voice_name or 'en-US_LisaV3Voice', lang=lang)
        client = TextToSpeechV1(authenticator=IAMAuthenticator(api_key))
        client.set_service_url(api_url)
        self.client = client

    def _synth(self, ssml: str, filename: str) -> None:
        resp = self.client.synthesize(
            text=ssml, voice=self.voice_name, accept='audio/wav')
        with open(filename, 'wb') as wav:
            content = resp.get_result().content

            wav.write(content)
