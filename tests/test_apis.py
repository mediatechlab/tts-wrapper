from tts_wrapper import PollyTTS, MicrosoftTTS
import os

POLLY_REGION = os.environ["POLLY_REGION"]
POLLY_AWS_ID = os.environ["POLLY_AWS_ID"]
POLLY_AWS_KEY = os.environ["POLLY_AWS_KEY"]
MICROSOFT_KEY = os.environ["MICROSOFT_KEY"]

CREDS = {
    PollyTTS: (POLLY_REGION, POLLY_AWS_ID, POLLY_AWS_KEY),
    MicrosoftTTS: MICROSOFT_KEY,
}


def test_real_synth():
    for cls, creds in CREDS.items():
        tts = cls()
        tts.set_credentials(creds)

        file_path = "/tmp/polly.mp3"
        assert not os.path.exists(file_path)
        tts.synth(tts.wrap_ssml("Hello, world!"), file_path)
        assert os.path.exists(file_path)
        assert os.path.getsize(file_path) > 1024
        os.unlink(file_path)
