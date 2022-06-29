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
    PicoClient,
    PicoTTS,
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
    PicoTTS: PicoClient(),
}


def test_actual_synth(helpers):
    for cls, client in CLIENTS.items():
        tts = cls(client=client)
        print("Using", cls)

        for format in cls.supported_formats():
            print("Testing format", format)
            file_path = helpers.create_tmp_filename(f"audio.{format}")
            assert not os.path.exists(file_path)
            try:
                text = "Hello, world!"
                if hasattr(tts, "ssml"):
                    text = tts.ssml.add(text)
                tts.synth_to_file(text, file_path, format=format)
                helpers.check_audio_file(file_path, format=format)
            except:
                print(f"Exception with class '{cls}' and format '{format}'.")
                raise
            finally:
                os.remove(file_path)
