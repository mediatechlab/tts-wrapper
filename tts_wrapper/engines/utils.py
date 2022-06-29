import wave
from io import BytesIO


def process_wav(raw: bytes) -> bytes:
    bio = BytesIO()
    with wave.open(bio, "wb") as wav:
        wav.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # type: ignore
        wav.writeframes(raw)
    return bio.getvalue()
