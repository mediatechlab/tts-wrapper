import os

import pytest
from tts_wrapper.exceptions import UnsupportedFileFormat


def test_string_synth(all_patched_tts, helpers):
    filename = helpers.create_tmp_filename("speech.wav")

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file("hello world", filename)
        helpers.check_audio_file(filename)
        os.remove(filename)


def test_ssml_synth(all_patched_tts, helpers):
    filename = helpers.create_tmp_filename("speech.wav")

    for tts in all_patched_tts:
        assert not os.path.exists(filename)
        tts.synth_to_file(tts.wrap_ssml("hello world"), filename)
        helpers.check_audio_file(filename)
        os.remove(filename)


def test_repeated_synth(all_patched_tts, helpers):
    filename = helpers.create_tmp_filename("speech.wav")

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
