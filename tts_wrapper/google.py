try:
    from google.cloud import texttospeech
    from google.oauth2 import service_account
except ImportError:
    texttospeech = None
    service_account = None

from .tts import TTS, ModuleNotInstalled


class GoogleTTS(TTS):
    def __init__(self, creds: str = None, voice_name=None, lang=None) -> None:
        '''
        @param creds: The path to the json file that contains the credentials. 
        If None, assumes that the environment variable is set.
        '''
        if texttospeech is None or service_account is None:
            raise ModuleNotInstalled('google-cloud-texttospeech')

        super().__init__(voice_name=voice_name or 'en-US-Wavenet-C', lang=lang)
        google_creds = service_account.Credentials.from_service_account_file(
            creds) if creds else None
        self.client = texttospeech.TextToSpeechClient(credentials=google_creds)

    def _synth(self, ssml: str, filename: str) -> None:
        # pylint: disable=no-member
        s_input = texttospeech.SynthesisInput(ssml=ssml)

        voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang,
            name=self.voice_name)

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        # pylint: enable=no-member

        resp = self.client.synthesize_speech(s_input, voice, audio_config)

        assert resp.audio_content

        with open(filename, 'wb') as f:
            f.write(resp.audio_content)
