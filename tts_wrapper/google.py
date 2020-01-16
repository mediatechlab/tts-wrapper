from google.cloud import texttospeech
from google.oauth2 import service_account

from .tts import TTS


class GoogleTTS(TTS):
    def __init__(self, creds: str = None, voice_name=None, lang=None) -> None:
        '''
        @param creds: The path to the json file that contains the credentials. 
        If None, assumes that the environment variable is set.
        '''
        super().__init__(voice_name=voice_name or 'en-US-Wavenet-C', lang=lang)
        google_creds = service_account.Credentials.from_service_account_file(
            creds) if creds else None
        self.client = texttospeech.TextToSpeechClient(credentials=google_creds)

    def _synth(self, ssml: str, filename: str) -> None:
        # pylint: disable=no-member
        s_input = texttospeech.types.SynthesisInput(ssml=ssml)

        voice = texttospeech.types.VoiceSelectionParams(
            language_code=self.lang,
            name=self.voice_name)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
        # pylint: enable=no-member

        resp = self.client.synthesize_speech(s_input, voice, audio_config)

        assert resp.audio_content

        with open(filename, 'wb') as f:
            f.write(resp.audio_content)
