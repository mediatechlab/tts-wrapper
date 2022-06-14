from tts_wrapper import PollyTTS
import os

POLLY_REGION = os.environ["POLLY_REGION"]
POLLY_AWS_ID = os.environ["POLLY_AWS_ID"]
POLLY_AWS_KEY = os.environ["POLLY_AWS_KEY"]


def test_polly_synth():
    polly = PollyTTS()
    polly.set_credentials((POLLY_REGION, POLLY_AWS_ID, POLLY_AWS_KEY))

    polly_path = "/tmp/polly.mp3"
    assert not os.path.exists(polly_path)
    polly.synth(polly.create_ssml_root().add("Hello, world!"), polly_path)
    assert os.path.exists(polly_path)
    os.unlink(polly_path)
