import wave

from .tts import ModuleNotInstalled, TTS

try:
    import boto3
except ImportError:
    boto3 = None


class AwsCredentials(object):
    def __init__(self, aws_key_id, aws_access_key, region=None) -> None:
        self.aws_key_id = aws_key_id
        self.aws_access_key = aws_access_key
        self.region = region


class PollyTTS(TTS):
    def __init__(self, creds: AwsCredentials = None, voice_name=None, lang=None) -> None:
        if boto3 is None:
            raise ModuleNotInstalled('boto3')

        super().__init__(voice_name=voice_name or 'Joanna', lang=lang)
        if creds:
            boto_session = boto3.Session(
                aws_access_key_id=creds.aws_key_id, aws_secret_access_key=creds.aws_access_key,
                region_name=creds.region)
        else:
            boto_session = boto3.Session()
        self.polly_client = boto_session.client('polly')

    def _synth(self, ssml: str, filename: str) -> None:
        resp = self.polly_client.synthesize_speech(Engine='neural',
                                                   OutputFormat='pcm',
                                                   VoiceId=self.voice_name,
                                                   TextType='ssml',
                                                   Text=ssml)

        with wave.open(filename, 'wb') as wav:
            # pylint: disable=no-member
            wav.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wav.writeframes(resp['AudioStream'].read())
