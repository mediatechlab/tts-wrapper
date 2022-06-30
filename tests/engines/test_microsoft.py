import os

import pytest
from tts_wrapper import MicrosoftClient, MicrosoftTTS

from . import BaseEngineTest


def create_client():
    MICROSOFT_KEY = os.environ.get("MICROSOFT_KEY")
    return MicrosoftClient(MICROSOFT_KEY)


@pytest.mark.parametrize("formats,tts_cls", [(["wav"], MicrosoftTTS)])
class TestMicrosoftOffline(BaseEngineTest):
    pass


@pytest.mark.slow
@pytest.mark.parametrize(
    "formats,tts_cls,client",
    [(MicrosoftTTS.supported_formats(), MicrosoftTTS, create_client)],
)
class TestMicrosoftOnline(BaseEngineTest):
    pass
