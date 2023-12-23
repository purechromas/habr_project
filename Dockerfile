FROM python:3.10 as base

LABEL creator="Blagovest Krasimirov Nedkov"
LABEL tags="PYTHON | DJANGO | CELERY | REDIS | BEAUTIFULSOUP | HTTPX"
LABEL version="0.0.1"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=10 \
    POETRY_VERSION=1.7.1

FROM base as builder

WORKDIR /habr/
COPY poetry.lock pyproject.toml /habr/
RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi 

COPY . /habr/