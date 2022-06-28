import os
import shutil

import pytest
from tts_wrapper.exceptions import UnsupportedFileFormat

TMP_DIR = "/tmp/tts-wrapper"
TMP_SPEECH = os.path.join(TMP_DIR, "speech.wav")


def setup_module():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR)


def test_string_synth(all_patched_tts, helpers):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file("hello world", filename)
        helpers.check_audio_file(filename)
        os.remove(filename)


def test_ssml_synth(all_patched_tts, helpers):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file(tts.wrap_ssml("hello world"), filename)
        helpers.check_audio_file(filename)
        os.remove(filename)


def test_repeated_synth(all_patched_tts, helpers):
    filename = TMP_SPEECH

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file("hello world", filename)
        helpers.check_audio_file(filename)
        os.remove(filename)

        tts.synth_to_file("bye world", filename)
        helpers.check_audio_file(filename)
        os.remove(filename)


def test_synth_unknown_format(all_patched_tts):
    for tts in all_patched_tts:
        pytest.raises(
            UnsupportedFileFormat, lambda: tts.synth_to_bytes("hello", format="unk")
        )
