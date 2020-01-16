import requests
from .tts import TTS


class MicrosoftTTS(TTS):
    def __init__(self, voice_name=None, lang=None, creds=None) -> None:
        super().__init__(voice_name=voice_name or 'en-US-JessaNeural', creds=creds, lang=lang)

    def _wrap_ssml(self, ssml) -> str:
        return (f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{self.lang}">'
                f'<voice name="{self.voice_name}">{ssml}</voice>'
                '</speak>')

    def _synth(self, ssml: str, filename: str) -> None:
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.creds
        }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }

        response = requests.post(
            'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1', headers=headers, data=ssml.encode('utf-8'))

        if response.status_code != 200:
            print('Server replied with', response.status_code)

        assert response.content

        with open(filename, 'wb') as wav:
            wav.write(response.content)
