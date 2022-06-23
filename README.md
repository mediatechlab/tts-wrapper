# TTS-Wrapper

![](https://github.com/mediatechlab/tts-wrapper/workflows/Python%20package/badge.svg)

_TTS-Wrapper_ is a hassle-free Python library that allows one to use text-to-speech APIs with the same interface.

Currently the following services are supported:

- AWS Polly
- Google TTS
- Microsoft TTS
- IBM Watson

## Installation

Install using pip.

```sh
pip install TTS-Wrapper
```

**Note: for each service you want to use, you have to install the required packages.**

Example: to use `google` and `watson`:

```sh
pip install TTS-Wrapper[google, watson]
```

## Usage

Simply instantiate an object from the desired service and call `synth()`.

```Python
from tts_wrapper import PollyTTS

tts = PollyTTS()
tts.synth('<speak>Hello, world!</speak>', 'hello.wav')
```

### Selecting a Voice

You can change the default voice by specifying the voice name and the language code:

```Python
tts.set_voice(voice_name='Camila', lang='pt-BR')
```

Check out the list of available voices for [Polly](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html), [Google](https://cloud.google.com/text-to-speech/docs/voices), [Microsoft](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices).

### SSML

You can also use [SSML](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) markup to control the output.

```Python
tts.synth('<speak>Hello, <break time="3s"/> world!</speak>', 'hello.wav')
```

As a convenience you can use the `wrap_ssml` function that will create the correct boilerplate tags for each engine:

```Python
tts = PollyTTS()
tts.synth(tts.wrap_ssml('Hello, <break time="3s"/> world!'), 'hello.wav')
```

Learn which tags are available for each service: [Polly](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html), [Google](https://cloud.google.com/text-to-speech/docs/ssml), [Microsoft](https://docs.microsoft.com/en-us/cortana/skills/speech-synthesis-markup-language), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-ssml).

### Credentials

To setup credentials to access each service, call the `set_credentials()` method.

#### Polly

If you don't explicitly define credentials, `boto3` will try to find them in your system's credentials file or your environment variables. However, you can specify them with a tuple:

```Python
from tts_wrapper import PollyTTS
tts = PollyTTS()
tts.set_credentials((region, aws_key_id, aws_access_key))
```

#### Google

Point to your [Oauth 2.0 credentials file](https://developers.google.com/identity/protocols/OAuth2) path:

```Python
from tts_wrapper import GoogleTTS
tts = GoogleTTS()
tts.set_credentials('path/to/creds.json')
```

#### Microsoft

Just provide your [subscription key](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#authentication), like so:

```Python
from tts_wrapper import MicrosoftTTS
tts = MicrosoftTTS()
tts.set_credentials('TOKEN')
```

If your region is not the default "useast", you can change it like so:

```Python
tts = MicrosoftTTS(region='brazilsouth')
```

#### Watson

Pass your [API key and URL](https://cloud.ibm.com/apidocs/text-to-speech/text-to-speech#authentication) to the initializer:

```Python
from tts_wrapper import WatsonTTS
tts = WatsonTTS
tts.set_credentials(('API_KEY', 'API_URL'))
```

## License

Licensed under the [MIT License](./LICENSE).
