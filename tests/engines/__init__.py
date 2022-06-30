import os

import pytest
from tts_wrapper import UnsupportedFileFormat


class BaseEngineTest:
    def test_synth_to_file(self, tts, helpers, formats, tmp_path):
        for format in formats:
            file_path = helpers.create_tmp_filename(tmp_path, f"audio.{format}")
            assert not os.path.exists(file_path)

            text = "Hello, world!"
            if hasattr(tts, "ssml"):
                text = tts.ssml.add(text)

            try:
                tts.synth_to_file(text, file_path, format=format)
                helpers.check_audio_file(file_path, format=format)
            finally:
                os.remove(file_path)

    def test_synth_unknown_format(self, tts, formats):
        pytest.raises(
            UnsupportedFileFormat, lambda: tts.synth_to_bytes("hello", format="unk")
        )
