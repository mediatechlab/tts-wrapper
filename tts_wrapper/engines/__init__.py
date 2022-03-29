from .google import GoogleTTS
from .microsoft import MicrosoftTTS
from .polly import PollyTTS
from .watson import WatsonTTS

ENGINES = [GoogleTTS, MicrosoftTTS, PollyTTS, WatsonTTS]
