import wave

from google.cloud import texttospeech
import requests


def polly_tts(text, filename, polly_client, options=None):
    options = options or {}

    resp = polly_client.synthesize_speech(Engine='neural',
                                          OutputFormat='pcm',
                                          TextType='ssml',
                                          Text=text, **options)

    with wave.open(filename, 'wb') as wav:
        # pylint: disable=no-member
        wav.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wav.writeframes(resp['AudioStream'].read())


def ms_tts(text, filename, sub_key):
    fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': sub_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'YOUR_RESOURCE_NAME'
    }

    response = requests.post(
        'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1', headers=headers, data=text.encode('utf-8'))

    if response.status_code != 200:
        print('Server replied with', response.status_code)

    assert response.content

    with open(filename, 'wb') as wav:
        wav.write(response.content)


def google_tts(text, filename, voice_name='en-US-Wavenet-C', options=None):
    options = options or {}
    client = texttospeech.TextToSpeechClient()

    # pylint: disable=no-member
    synthesis_input = texttospeech.types.SynthesisInput(ssml=text)

    voice = texttospeech.types.VoiceSelectionParams(name=voice_name, **options)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    assert response.audio_content

    with open(filename, 'wb') as wav:
        wav.write(response.audio_content)
