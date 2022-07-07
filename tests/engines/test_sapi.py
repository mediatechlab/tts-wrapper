import os
import sys

import pytest
from tts_wrapper import SAPITTS, SAPIClient

from . import BaseEngineTest


def create_client():
    return SAPIClient()


@pytest.mark.parametrize("formats,tts_cls", [(["wav"], SAPITTS)])
class TestSAPIOffline(BaseEngineTest):
    pass


@pytest.mark.slow
@pytest.mark.skipif(
    not sys.platform.startswith("win") or "CI" in os.environ,
    reason="Skipping SAPI synth because it is windows-only (can only run on a box).",
)
@pytest.mark.parametrize(
    "formats,tts_cls,client",
    [(SAPITTS.supported_formats(), SAPITTS, create_client)],
)
class TestSAPIOnline(BaseEngineTest):
    pass
