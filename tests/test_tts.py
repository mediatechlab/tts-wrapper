from contextlib import contextmanager
import os
import pickle
from unittest.mock import MagicMock

from tts_wrapper import GoogleTTS, MicrosoftTTS, PollyTTS


TEST_DIR = '/tmp/tts-wrapper'
TEST_FILE = os.path.join(TEST_DIR, 'speech.wav')
TEST_DATA_DIR = os.path.join('tests', 'data')


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


def test_polly():
    resp = load_pickle(os.path.join(TEST_DATA_DIR, 'polly.pickle'))
    with managed_tts(PollyTTS) as tts:
        tts.polly_client = MagicMock()
        synth_resp = tts.polly_client.synthesize_speech.return_value
        synth_resp['AudioStream'] = MagicMock()
        synth_resp['AudioStream'].read.return_value = resp

        tts.synth('hello world', TEST_FILE)


def patch_microsoft_tts(mocker, tts):
    resp = load_pickle(os.path.join(TEST_DATA_DIR, 'microsoft.pickle'))
    mock_post = mocker.patch('requests.post')
    mocked_resp = mock_post.return_value
    mocked_resp.status_code = 200
    mocked_resp.content = resp

    tts._fetch_access_token = MagicMock()
    tts._fetch_access_token.return_value = 'mocked-access-token'


def test_microsoft(mocker):
    with managed_tts(MicrosoftTTS, creds='fakecreds') as tts:
        patch_microsoft_tts(mocker, tts)
        tts.synth('hello world', TEST_FILE)


def test_microsoft_repeated_synth(mocker):
    with managed_tts(MicrosoftTTS, creds='fakecreds') as tts:
        patch_microsoft_tts(mocker, tts)
        tts.synth('hello world', TEST_FILE)
        check_audio_file(TEST_FILE)
        os.remove(TEST_FILE)
        tts.synth('bye world', TEST_FILE)


def test_google(mocker):
    resp = load_pickle(os.path.join(TEST_DATA_DIR, 'google.pickle'))
    mocked_client = mocker.patch(
        'google.cloud.texttospeech.TextToSpeechClient')
    google_resp = mocked_client.return_value.synthesize_speech.return_value
    google_resp.audio_content = resp

    with managed_tts(GoogleTTS) as tts:
        tts.synth('hello world', TEST_FILE)
