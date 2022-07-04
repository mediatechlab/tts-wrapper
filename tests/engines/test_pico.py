import sys
import pytest
from tts_wrapper import PicoClient, PicoTTS

from . import BaseEngineTest


def create_client():
    return PicoClient()


@pytest.mark.parametrize("formats,tts_cls", [(["wav"], PicoTTS)])
class TestPicoOffline(BaseEngineTest):
    pass


@pytest.mark.slow
@pytest.mark.skipif(
    sys.platform != "linux",
    reason="Skipping PicoTTS synth because it is linux-only.",
)
@pytest.mark.parametrize(
    "formats,tts_cls,client",
    [(PicoTTS.supported_formats(), PicoTTS, create_client)],
)
class TestPicoOnline(BaseEngineTest):
    pass
