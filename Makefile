.PHONY: api_tests tests publish act-build cov.xml

tests:
	poetry run pytest tests/test_ssml.py tests/test_tts.py

api_tests:
	source .secrets/.env && \
	export POLLY_REGION POLLY_AWS_ID POLLY_AWS_KEY && \
	export MICROSOFT_KEY && \
	export GOOGLE_SA_PATH && \
	export WATSON_API_KEY WATSON_API_URL && \
	poetry run pytest -s tests/test_apis.py

publish:
	poetry publish --build

act-build:
	act --secret-file .secrets/.env -a build

requirements.txt: pyproject.toml
	poetry export --without-hashes -E google -E watson -E polly -E microsoft -f requirements.txt -o requirements.txt

requirements.dev.txt: pyproject.toml requirements.txt
	poetry export --dev --without-hashes -f requirements.txt -o requirements.dev.txt

cov.xml:
	poetry run pytest --cov-report xml:cov.xml --cov=tts_wrapper tests/test_tts.py  tests/test_ssml.py