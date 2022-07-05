import os
import random
import string
import tempfile
import wave
from io import BytesIO


def process_wav(raw: bytes) -> bytes:
    bio = BytesIO()
    with wave.open(bio, "wb") as wav:
        wav.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # type: ignore
        wav.writeframes(raw)
    return bio.getvalue()


def create_temp_filename(suffix="") -> str:
    random_seq = "".join(random.choice(string.ascii_letters) for _ in range(10))
    return os.path.join(
        tempfile.gettempdir(), f"{tempfile.gettempprefix()}_{random_seq}{suffix}"
    )
