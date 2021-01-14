.PHONY: tests publish

tests:
	poetry run pytest

publish:
	poetry publish --build

requirements.txt: pyproject.toml
	poetry export --dev --without-hashes -f requirements.txt > requirements.txt
