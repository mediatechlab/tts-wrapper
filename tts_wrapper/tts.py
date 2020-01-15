from enum import Enum
from typing import cast
import boto3
from .backends import polly_tts, ms_tts, google_tts


class BackendEnum(Enum):
    POLLY = 'polly'
    MICROSOFT = 'microsoft'
    GOOGLE = 'google'


DEFAULT_VOICE_NAMES = {
    BackendEnum.POLLY: 'Joanna',
    BackendEnum.MICROSOFT: 'en-US-JessaNeural',
    BackendEnum.GOOGLE: 'en-US-Wavenet-C'
}


class AwsCredentials(object):
    def __init__(self, aws_key_id, aws_access_key) -> None:
        self.aws_key_id = aws_key_id
        self.aws_access_key = aws_access_key


class TTS(object):
    def __init__(self, backend: BackendEnum, voice_name=None, creds=None, lang=None) -> None:
        '''
        @param backend: the voice backend to use.
        @param voice_name: the voice identifier to use (we have a default value if you don't care).
        @param creds: the credentials for the service that you are using.
        '''
        self.backend = backend
        self.creds = creds
        self.polly_client = None
        self.voice_name = voice_name or DEFAULT_VOICE_NAMES[backend]
        self.lang = lang or 'en-US'

        if self.backend == BackendEnum.POLLY:
            if self.creds:
                creds = cast(AwsCredentials, creds)
                boto_session = boto3.Session(
                    aws_access_key_id=creds.aws_key_id, aws_secret_access_key=creds.aws_access_key)
            else:
                boto_session = boto3.Session()
            self.polly_client = boto_session.client('polly')

    def __wrap_ssml(self, ssml) -> str:
        if self.backend == BackendEnum.MICROSOFT:
            return (f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{self.lang}">'
                    f'<voice name="{self.voice_name}">{ssml}</voice>'
                    '</speak>')
        else:
            return f'<speak>{ssml}</speak>'

    def synth(self, ssml: str, filename: str) -> None:
        '''
        @param filename: the output wave file path.
        @param ssml: the ssml text to synthesize without the speak tag (will be added automatically).
        '''
        wrapped_ssml = self.__wrap_ssml(ssml)

        if self.backend == BackendEnum.POLLY:
            polly_tts(wrapped_ssml, filename, self.polly_client,
                      options=dict(VoiceId=self.voice_name))

        elif self.backend == BackendEnum.MICROSOFT:
            ms_tts(wrapped_ssml, filename, self.creds)

        elif self.backend == BackendEnum.GOOGLE:
            google_tts(wrapped_ssml, filename, options=None)
