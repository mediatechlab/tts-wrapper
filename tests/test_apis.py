import os

from tts_wrapper import (
    GoogleClient,
    GoogleTTS,
    MicrosoftClient,
    MicrosoftTTS,
    PollyClient,
    PollyTTS,
    WatsonClient,
    WatsonTTS,
)

POLLY_REGION = os.environ["POLLY_REGION"]
POLLY_AWS_ID = os.environ["POLLY_AWS_ID"]
POLLY_AWS_KEY = os.environ["POLLY_AWS_KEY"]
MICROSOFT_KEY = os.environ["MICROSOFT_KEY"]
GOOGLE_SA_PATH = os.environ["GOOGLE_SA_PATH"]
WATSON_API_KEY = os.environ["WATSON_API_KEY"]
WATSON_API_URL = os.environ["WATSON_API_URL"]

CLIENTS = {
    PollyTTS: PollyClient((POLLY_REGION, POLLY_AWS_ID, POLLY_AWS_KEY)),
    MicrosoftTTS: MicrosoftClient(MICROSOFT_KEY),
    GoogleTTS: GoogleClient(GOOGLE_SA_PATH),
    WatsonTTS: WatsonClient((WATSON_API_KEY, WATSON_API_URL)),
}


def test_actual_synth():
    for cls, client in CLIENTS.items():
        tts = cls(client=client)

        file_path = "/tmp/audio.mp3"
        assert not os.path.exists(file_path)
        try:
            tts.synth_to_file(tts.wrap_ssml("Hello, world!"), file_path)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) > 1024
        finally:
            os.unlink(file_path)
