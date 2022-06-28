import os
from unittest.mock import MagicMock

import pytest
from tts_wrapper.engines import ENGINES

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TEST_DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def load_resp_wav():
    with open(os.path.join(TEST_DATA_DIR, "test.wav"), "rb") as f:
        return f.read()


class Helpers:
    @staticmethod
    def check_audio_file(path):
        assert os.path.exists(path), f"{path} does not exists"
        assert os.path.getsize(path) > 1024


@pytest.fixture(scope="session")
def helpers():
    return Helpers


@pytest.fixture(scope="module")
def client():
    client = MagicMock()
    client.synth.return_value = load_resp_wav()
    return client


@pytest.fixture(scope="module")
def all_patched_tts(client):
    return [engine(client=client) for engine in ENGINES]
