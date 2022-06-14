.PHONY: api_tests tests publish

tests:
	poetry run pytest tests/test_ssml.py tests/test_tts.py

api_tests:
	source .secrets/.env && \
	export POLLY_REGION POLLY_AWS_ID POLLY_AWS_KEY && \
	poetry run pytest tests/test_apis.py

publish:
	poetry publish --build

requirements.txt: pyproject.toml
	poetry export --without-hashes -E google -E watson -E polly -E microsoft -f requirements.txt -o requirements.txt