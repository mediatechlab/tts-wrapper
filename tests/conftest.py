import os
from typing import Callable
from unittest.mock import MagicMock

import filetype  # type: ignore
import pytest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def load_resp_wav():
    with open(os.path.join(TEST_DATA_DIR, "test.wav"), "rb") as f:
        return f.read()


class Helpers:
    @staticmethod
    def check_audio_file(path, format="wav"):
        assert os.path.exists(path), f"{path} does not exists"
        assert os.path.getsize(path) > 1024
        assert filetype.guess_extension(path) == format

    @staticmethod
    def create_tmp_filename(tmp_dir, filename):
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        return os.path.join(tmp_dir, filename)


@pytest.fixture(scope="session")
def helpers():
    return Helpers


@pytest.fixture(scope="module")
def client():
    client = MagicMock()
    client.synth.return_value = load_resp_wav()
    return client


@pytest.fixture()
def tts(tts_cls, client):
    if isinstance(client, Callable) and not isinstance(client, MagicMock):
        client = client()
    return tts_cls(client=client)
