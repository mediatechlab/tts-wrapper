from contextlib import contextmanager
import os

from tts_wrapper import AwsCredentials, MicrosoftTTS, PollyTTS, GoogleTTS

TEST_DIR = '/tmp/tts-wrapper'
TEST_FILE = os.path.join(TEST_DIR, 'file.wav')
SECRETS_DIR = '.secrets'


def load_test_aws_creds():
    with open(os.path.join(SECRETS_DIR, 'aws')) as f:
        lines = [l.strip() for l in f.readlines()]
        return AwsCredentials(lines[0], lines[1])


def load_test_ms_creds():
    with open(os.path.join(SECRETS_DIR, 'microsoft')) as f:
        return f.read().strip()


def load_test_google_creds():
    return os.path.join(SECRETS_DIR, 'google.json')


@contextmanager
def managed_tts(cls, *args, **kwargs):
    tts = cls(*args, **kwargs)
    assert not os.path.exists(TEST_FILE)
    try:
        yield tts
    finally:
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)


def setup_module():
    os.makedirs(TEST_DIR, exist_ok=True)


def test_polly_with_defaults():
    with managed_tts(PollyTTS) as tts:
        tts.synth('hello world', TEST_FILE)
        assert os.path.exists(TEST_FILE)


def test_polly_with_creds():
    creds = load_test_aws_creds()
    with managed_tts(PollyTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)
        assert os.path.exists(TEST_FILE)


def test_microsoft_with_creds():
    creds = load_test_ms_creds()
    with managed_tts(MicrosoftTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)
        assert os.path.exists(TEST_FILE)


def test_microsoft_repeated_synth():
    creds = load_test_ms_creds()
    with managed_tts(MicrosoftTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)
        assert os.path.exists(TEST_FILE)
        os.remove(TEST_FILE)
        tts.synth('bye world', TEST_FILE)
        assert os.path.exists(TEST_FILE)


def test_google_with_creds():
    creds = load_test_google_creds()
    with managed_tts(GoogleTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)
        assert os.path.exists(TEST_FILE)
