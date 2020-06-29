class TTSWException(Exception):
    pass


class SynthError(TTSWException):
    pass


class ModuleNotInstalled(TTSWException):
    def __init__(self, module: str) -> None:
        message = f'Module {module} is not installed. It is not included with tts-wrapper.'
        super().__init__(message)


class TTS(object):
    def __init__(self, voice_name=None, lang=None) -> None:
        '''
        @param voice_name: the voice identifier to use (we have a default value if you don't care).
        @param lang: language code (should match the voice_name).
        '''
        self.voice_name = voice_name
        self.lang = lang or 'en-US'

    def _wrap_ssml(self, ssml) -> str:
        return f'<speak>{ssml}</speak>'

    def _synth(self, ssml: str, filename: str) -> None:
        raise NotImplementedError()

    def synth(self, ssml: str, filename: str) -> None:
        '''
        @param ssml: the ssml text to synthesize without the speak tag (will be added automatically).
        @param filename: the output wave file path.
        '''
        wrapped_ssml = self._wrap_ssml(ssml)
        try:
            self._synth(wrapped_ssml, filename)
        except Exception as e:
            raise SynthError(
                f'Error while calling synth with "{(ssml[:100] + "...") if len(ssml) > 100 else ssml}"') from e
