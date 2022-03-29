.PHONY: tests publish

tests:
	poetry run pytest

publish:
	poetry publish --build

requirements.txt: pyproject.toml
	poetry export --without-hashes -E google -E watson -E polly -E microsoft -f requirements.txt -o requirements.txt