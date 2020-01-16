from google.cloud import texttospeech
from .tts import TTS


class GoogleTTS(TTS):
    def __init__(self, voice_name=None, lang=None, creds=None) -> None:
        super().__init__(voice_name=voice_name or 'en-US-Wavenet-C', creds=creds, lang=lang)

    def _synth(self, ssml: str, filename: str) -> None:
        options = dict(VoiceId=self.voice_name)
        client = texttospeech.TextToSpeechClient()

        # pylint: disable=no-member
        synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml)

        voice = texttospeech.types.VoiceSelectionParams(
            name=self.voice_name, **options)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
        # pylint: enable=no-member

        response = client.synthesize_speech(
            synthesis_input, voice, audio_config)

        assert response.audio_content

        with open(filename, 'wb') as wav:
            wav.write(response.audio_content)
