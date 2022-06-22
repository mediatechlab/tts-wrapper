import os
import pickle
import shutil
import pytest
from unittest.mock import MagicMock

from tts_wrapper import GoogleTTS, MicrosoftTTS, PollyTTS, WatsonTTS

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TMP_DIR = "/tmp/tts-wrapper"
TMP_SPEECH = os.path.join(TMP_DIR, "speech.wav")
TEST_DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def load_resp_wav():
    with open(os.path.join(TEST_DATA_DIR, "test.wav"), "rb") as f:
        return f.read()


def check_audio_file(path):
    assert os.path.exists(path), f"{path} does not exists"
    assert os.path.getsize(path) > 0


@pytest.fixture
def patched_polly():
    tts = PollyTTS()
    tts.client = MagicMock()
    synth_resp = tts.client.synthesize_speech.return_value
    synth_resp["AudioStream"] = MagicMock()
    synth_resp["AudioStream"].read.return_value = load_pickle(
        os.path.join(TEST_DATA_DIR, "polly.pickle")
    )
    return tts


@pytest.fixture
def patched_ms():
    resp = load_resp_wav()
    tts = MicrosoftTTS()
    tts.sess = MagicMock()
    tts.sess.post.return_value = MagicMock()
    tts.sess.post.return_value.status_code = 200
    tts.sess.post.return_value.content = resp

    tts._fetch_access_token = MagicMock()
    tts._fetch_access_token.return_value = "mocked-access-token"
    return tts


@pytest.fixture
def patched_google(mocker):
    resp = load_resp_wav()
    mocked_client = mocker.patch("google.cloud.texttospeech.TextToSpeechClient")
    mocked_client.return_value.synthesize_speech.return_value.audio_content = resp

    from tts_wrapper.engines.google.google import texttospeech

    tts = GoogleTTS()
    tts.client = texttospeech.TextToSpeechClient(None)
    return tts


@pytest.fixture
def patched_watson():
    resp = load_resp_wav()
    tts = WatsonTTS()
    tts.client = MagicMock()
    tts.client.synthesize.return_value.get_result.return_value.content = resp
    return tts


@pytest.fixture
def all_patched_tts(patched_polly, patched_ms, patched_google, patched_watson):
    return [patched_polly, patched_ms, patched_google, patched_watson]


def setup_module():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)


def test_string_synth(all_patched_tts):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth("hello world", filename)
        check_audio_file(filename)
        os.remove(filename)


def test_ssml_synth(all_patched_tts):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth(tts.wrap_ssml("hello world"), filename)
        check_audio_file(filename)
        os.remove(filename)


def test_repeated_synth(all_patched_tts):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth("hello world", filename)
        check_audio_file(filename)
        os.remove(filename)

        tts.synth("bye world", filename)
        check_audio_file(filename)
        os.remove(filename)
