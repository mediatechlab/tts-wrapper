import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

setup(
    name='TTS-Wrapper',
    version='0.4.1',
    packages=['tts_wrapper'],
    install_requires=[],
    extra_requires={
        'google': ['google-cloud-texttospeech>=0.5'],
        'polly': ['boto3>=1'],
        'watson': ['ibm_watson>=4.3'],
        'microsoft': ['requests>=2']
    },
    license='MIT',

    author='Giulio Bottari',
    author_email='giuliobottari@gmail.com',
    description='A hassle-free Python library that allows one to use text-to-speech APIs with the same interface',
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    keywords='tts text-to-speech lib library api',
    url='https://github.com/mediatechlab/tts-wrapper',
    project_urls={
        'Bus Tracker': 'https://github.com/mediatechlab/tts-wrapper/issues',
        'Documentation': 'https://github.com/mediatechlab/tts-wrapper/blob/master/README.md',
        'Source Code': 'https://github.com/mediatechlab/tts-wrapper'
    },
)
