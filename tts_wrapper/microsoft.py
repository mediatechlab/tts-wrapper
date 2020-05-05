try:
    import requests
except ImportError:
    requests = None

from .tts import ModuleNotInstalled, TTS


class MicrosoftTTS(TTS):
    def __init__(self, creds: str, voice_name=None, lang=None) -> None:
        if requests is None:
            raise ModuleNotInstalled('requests')

        super().__init__(voice_name=voice_name or 'en-US-JessaNeural', lang=lang)
        self.access_token = None
        self.creds = creds

    def _wrap_ssml(self, ssml) -> str:
        return (f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{self.lang}">'
                f'<voice name="{self.voice_name}">{ssml}</voice>'
                '</speak>')

    def _fetch_access_token(self):
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.creds
        }
        response = requests.post(fetch_token_url, headers=headers)
        return str(response.text)

    def _synth(self, ssml: str, filename: str) -> None:
        if not self.access_token:
            self.access_token = self._fetch_access_token()

        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        }

        response = requests.post(
            'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1', headers=headers, data=ssml.encode('utf-8'))

        if response.status_code != 200:
            raise Exception(f'Server replied with {response.status_code}')

        assert response.content

        with open(filename, 'wb') as wav:
            wav.write(response.content)
