import os
import shutil
import pytest
from unittest.mock import MagicMock

from tts_wrapper import GoogleTTS, MicrosoftTTS, PollyTTS, WatsonTTS

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TMP_DIR = "/tmp/tts-wrapper"
TMP_SPEECH = os.path.join(TMP_DIR, "speech.wav")
TEST_DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def load_resp_wav():
    with open(os.path.join(TEST_DATA_DIR, "test.wav"), "rb") as f:
        return f.read()


def check_audio_file(path):
    assert os.path.exists(path), f"{path} does not exists"
    assert os.path.getsize(path) > 0


@pytest.fixture
def patched_polly():
    client = MagicMock()
    tts = PollyTTS(client)
    client.synth.return_value = load_resp_wav()
    return tts


@pytest.fixture
def patched_ms():
    client = MagicMock()
    client.synth.return_value = load_resp_wav()
    return MicrosoftTTS(client=client)


@pytest.fixture
def patched_google():
    client = MagicMock()
    client.synth.return_value = load_resp_wav()
    return GoogleTTS(client=client)


@pytest.fixture
def patched_watson():
    client = MagicMock()
    client.synth.return_value = load_resp_wav()
    return WatsonTTS(client=client)


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
        tts.synth_to_file("hello world", filename)
        check_audio_file(filename)
        os.remove(filename)


def test_ssml_synth(all_patched_tts):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file(tts.wrap_ssml("hello world"), filename)
        check_audio_file(filename)
        os.remove(filename)


def test_repeated_synth(all_patched_tts):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file("hello world", filename)
        check_audio_file(filename)
        os.remove(filename)

        tts.synth_to_file("bye world", filename)
        check_audio_file(filename)
        os.remove(filename)
