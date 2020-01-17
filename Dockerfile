FROM python:3.6.10-alpine3.10

WORKDIR /app

COPY setup.py requirements.txt /app/
COPY tests/requirements.txt /app/tests/

RUN apk add --no-cache build-base && \
  pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt && \
  pip install --no-cache-dir --trusted-host pypi.python.org -r /app/tests/requirements.txt

COPY tests /app/tests
COPY tts_wrapper /app/tts_wrapper/

# Run tests
RUN pytest tests/test_tts.py

# Run lib setup
RUN python setup.py install

# Try using the lib
RUN python tests/lib_test.py