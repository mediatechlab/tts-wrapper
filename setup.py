import pathlib

from setuptools import setup  # type: ignore

HERE = pathlib.Path(__file__).parent

setup(
    name="TTS-Wrapper",
    version="0.7.0",
    packages=["tts_wrapper"],
    install_requires=[],
    extras_require={
        "google": ["google-cloud-texttospeech>=2"],
        "polly": ["boto3>=1"],
        "watson": ["ibm_watson>=6"],
        "microsoft": ["requests>=2"],
    },
    license="MIT",
    author="Giulio Bottari",
    author_email="giuliobottari@gmail.com",
    description="TTS-Wrapper makes it easier to use text-to-speech APIs by providing a unified and easy-to-use interface.",
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    keywords="tts text-to-speech lib library api",
    url="https://github.com/mediatechlab/tts-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/mediatechlab/tts-wrapper/issues",
        "Documentation": "https://github.com/mediatechlab/tts-wrapper/blob/master/README.md",
        "Source Code": "https://github.com/mediatechlab/tts-wrapper",
    },
)
