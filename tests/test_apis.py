import os

from tts_wrapper import GoogleTTS, MicrosoftTTS, PollyTTS, WatsonTTS

POLLY_REGION = os.environ["POLLY_REGION"]
POLLY_AWS_ID = os.environ["POLLY_AWS_ID"]
POLLY_AWS_KEY = os.environ["POLLY_AWS_KEY"]
MICROSOFT_KEY = os.environ["MICROSOFT_KEY"]
GOOGLE_SA_PATH = os.environ["GOOGLE_SA_PATH"]
WATSON_API_KEY = os.environ["WATSON_API_KEY"]
WATSON_API_URL = os.environ["WATSON_API_URL"]

CREDS = {
    PollyTTS: (POLLY_REGION, POLLY_AWS_ID, POLLY_AWS_KEY),
    MicrosoftTTS: MICROSOFT_KEY,
    GoogleTTS: GOOGLE_SA_PATH,
    WatsonTTS: (WATSON_API_KEY, WATSON_API_URL),
}


def test_actual_synth():
    for cls, creds in CREDS.items():
        tts = cls(credentials=creds)

        file_path = "/tmp/audio.mp3"
        assert not os.path.exists(file_path)
        try:
            tts.synth(tts.wrap_ssml("Hello, world!"), file_path)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) > 1024
        finally:
            os.unlink(file_path)
