from tts_wrapper import PollyTTS, MicrosoftTTS
import os

POLLY_REGION = os.environ["POLLY_REGION"]
POLLY_AWS_ID = os.environ["POLLY_AWS_ID"]
POLLY_AWS_KEY = os.environ["POLLY_AWS_KEY"]
MICROSOFT_KEY = os.environ["MICROSOFT_KEY"]


def test_polly_synth():
    polly = PollyTTS()
    polly.set_credentials((POLLY_REGION, POLLY_AWS_ID, POLLY_AWS_KEY))

    polly_path = "/tmp/polly.mp3"
    assert not os.path.exists(polly_path)
    polly.synth(polly.create_ssml_root().add("Hello, world!"), polly_path)
    assert os.path.exists(polly_path)
    os.unlink(polly_path)


def test_microsoft_synth():
    ms = MicrosoftTTS()
    ms.set_credentials(MICROSOFT_KEY)

    ms_path = "/tmp/ms.wav"
    assert not os.path.exists(ms_path)
    root = ms.create_ssml_root()
    root.children[0].add("Hello, world!")
    ms.synth(root, ms_path)
    assert os.path.exists(ms_path)
    os.unlink(ms_path)
