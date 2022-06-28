import os

import filetype  # type: ignore
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


def test_actual_synth(helpers):
    for cls, client in CLIENTS.items():
        tts = cls(client=client)

        file_path = "/tmp/audio.wav"
        assert not os.path.exists(file_path)
        try:
            tts.synth_to_file(tts.wrap_ssml("Hello, world!"), file_path)
            helpers.check_audio_file(file_path)
            assert filetype.guess_extension(file_path) == "wav"
        except:
            print("Exception with class", cls)
            raise
        finally:
            os.remove(file_path)
