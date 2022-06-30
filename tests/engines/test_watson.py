import os

import pytest
from tts_wrapper import WatsonClient, WatsonTTS

from . import BaseEngineTest


def create_client():
    WATSON_API_KEY = os.environ.get("WATSON_API_KEY")
    WATSON_API_URL = os.environ.get("WATSON_API_URL")
    return WatsonClient((WATSON_API_KEY, WATSON_API_URL))


@pytest.mark.parametrize("formats,tts_cls", [(["wav"], WatsonTTS)])
class TestWatsonOffline(BaseEngineTest):
    pass


@pytest.mark.slow
@pytest.mark.parametrize(
    "formats,tts_cls,client",
    [(WatsonTTS.supported_formats(), WatsonTTS, create_client)],
)
class TestWatsonOnline(BaseEngineTest):
    pass
