from contextlib import contextmanager
import os
import pickle
import shutil
from unittest.mock import MagicMock
import pytest

from tts_wrapper import (
    AwsCredentials, GoogleTTS, MicrosoftTTS, PollyTTS, WatsonTTS)


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TMP_DIR = '/tmp/tts-wrapper'
TMP_SPEECH = os.path.join(TMP_DIR, 'speech.wav')
TEST_DATA_DIR = os.path.join(SCRIPT_DIR, 'data')


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def load_resp_wav():
    with open(os.path.join(TEST_DATA_DIR, 'test.wav'), 'rb') as f:
        return f.read()


def check_audio_file(path):
    assert os.path.exists(path), f'{path} does not exists'
    assert os.path.getsize(path) > 0


@contextmanager
def managed_tts(cls, *args, _filename=TMP_SPEECH, **kwargs):
    tts = cls(*args, **kwargs)
    assert not os.path.exists(_filename)
    try:
        yield tts
    finally:
        check_audio_file(_filename)
        if os.path.exists(_filename):
            os.remove(_filename)


def setup_module():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)


def test_polly():
    resp = load_pickle(os.path.join(TEST_DATA_DIR, 'polly.pickle'))
    creds = AwsCredentials('AWS_ID', 'AWS_KEY', region='us-east-1')

    with managed_tts(PollyTTS, creds=creds) as tts:
        tts.polly_client = MagicMock()
        synth_resp = tts.polly_client.synthesize_speech.return_value
        synth_resp['AudioStream'] = MagicMock()
        synth_resp['AudioStream'].read.return_value = resp

        tts.synth('hello world', TMP_SPEECH)


def patch_microsoft_tts(mocker, tts):
    resp = load_resp_wav()
    mock_post = mocker.patch('requests.post')
    mocked_resp = mock_post.return_value
    mocked_resp.status_code = 200
    mocked_resp.content = resp

    tts._fetch_access_token = MagicMock()
    tts._fetch_access_token.return_value = 'mocked-access-token'


def test_microsoft(mocker):
    with managed_tts(MicrosoftTTS, creds='fakecreds') as tts:
        patch_microsoft_tts(mocker, tts)
        tts.synth('hello world', TMP_SPEECH)


def test_microsoft_repeated_synth(mocker):
    with managed_tts(MicrosoftTTS, creds='fakecreds') as tts:
        patch_microsoft_tts(mocker, tts)
        tts.synth('hello world', TMP_SPEECH)
        check_audio_file(TMP_SPEECH)
        os.remove(TMP_SPEECH)
        tts.synth('bye world', TMP_SPEECH)


def test_google(mocker):
    resp = load_resp_wav()
    mocked_client = mocker.patch(
        'google.cloud.texttospeech.TextToSpeechClient')
    mocked_client.return_value.synthesize_speech.return_value.audio_content = resp

    with managed_tts(GoogleTTS) as tts:
        tts.synth('hello world', TMP_SPEECH)


def test_watson(mocker):
    resp = load_resp_wav()
    with managed_tts(WatsonTTS, api_key='api_key', api_url='api_url') as tts:
        tts.client = MagicMock()
        tts.client.synthesize.return_value.get_result.return_value.content = resp
        tts.synth('hello world', TMP_SPEECH)
