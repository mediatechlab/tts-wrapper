from contextlib import contextmanager
import os
import pickle
from unittest.mock import MagicMock

from tts_wrapper import AwsCredentials, GoogleTTS, MicrosoftTTS, PollyTTS

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


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def check_audio_file(path):
    assert os.path.exists(path), f'{path} does not exists'
    assert os.path.getsize(path) > 0


@contextmanager
def managed_tts(cls, *args, _filename=TEST_FILE, **kwargs):
    tts = cls(*args, **kwargs)
    assert not os.path.exists(_filename)
    try:
        yield tts
    finally:
        check_audio_file(_filename)
        if os.path.exists(_filename):
            os.remove(_filename)


def setup_module():
    os.makedirs(TEST_DIR, exist_ok=True)


def test_polly_with_defaults():
    with managed_tts(PollyTTS) as tts:
        tts.synth('hello world', TEST_FILE)


def test_polly_with_creds():
    creds = load_test_aws_creds()
    with managed_tts(PollyTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)


def test_microsoft(mocker):
    resp = load_pickle('tests/microsoft_success.pickle')
    mock_post = mocker.patch('requests.post')
    mocked_resp = mock_post.return_value
    mocked_resp.status_code = 200
    mocked_resp.content = resp

    with managed_tts(MicrosoftTTS, creds='fakecreds') as tts:
        tts._fetch_access_token = MagicMock()
        mocked_access_token = tts._fetch_access_token.return_value
        mocked_access_token.return_value = 'mocked-access-token'
        tts.synth('hello world', TEST_FILE)


def test_microsoft_repeated_synth():
    creds = load_test_ms_creds()
    with managed_tts(MicrosoftTTS, creds=creds) as tts:
        tts.synth('hello world', TEST_FILE)
        check_audio_file(TEST_FILE)
        os.remove(TEST_FILE)
        tts.synth('bye world', TEST_FILE)


def test_google(mocker):
    resp = load_pickle('tests/google_success.pickle')
    mocked_client = mocker.patch(
        'google.cloud.texttospeech.TextToSpeechClient')
    google_resp = mocked_client.return_value.synthesize_speech.return_value
    google_resp.audio_content = resp

    with managed_tts(GoogleTTS) as tts:
        tts.synth('hello world', TEST_FILE)
