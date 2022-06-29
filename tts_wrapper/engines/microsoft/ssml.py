from ...ssml import BaseSSMLRoot, SSMLNode


class MicrosoftSSML(BaseSSMLRoot):
    def __init__(self, lang: str, voice: str) -> None:
        self.inner = SSMLNode("voice", {"name": voice})
        self.root = SSMLNode(
            "speak",
            {
                "version": "1.0",
                "xml:lang": lang,
                "xmlns": "https://www.w3.org/2001/10/synthesis",
                "xmlns:mstts": "https://www.w3.org/2001/mstts",
            },
        ).add(self.inner)
