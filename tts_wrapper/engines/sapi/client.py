import tempfile

from ...exceptions import ModuleNotInstalled

import pyttsx3  # type: ignore


class SAPIClient:
    def __init__(self) -> None:
        try:
            self._client = pyttsx3.init("sapi5")
        except ModuleNotFoundError:
            raise ModuleNotInstalled("sapi")

    def synth(self, text: str) -> bytes:
        with tempfile.NamedTemporaryFile("w+b", suffix=".wav") as temp:
            self._client.save_to_file(text, temp.name)
            self._client.runAndWait()
            temp.seek(0)
            return temp.read()
