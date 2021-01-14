.PHONY: build-lib upload-testing upload tests

build-lib: .stamps/lib

tests:
	poetry run pytest

upload-testing: .stamps/lib
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: .stamps/lib
	twine upload dist/*

.stamps/lib: .stamps/ tts_wrapper/* README.md requirements.txt setup.py
	mkdir -p .stamps
	rm -r build/ dist/ || /bin/true
	python setup.py bdist_wheel
	twine check dist/*
	touch .stamps/lib

requirements.txt: pyproject.toml
	poetry export --dev --without-hashes -f requirements.txt > requirements.txt
