FROM python:3.10.4-slim-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PATH=$PATH:/root/.local/bin \
    DJANGO_SETTINGS_MODULE="meme_generator.settings"

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        jq \
        less \
        libffi-dev \
        libpcre3 \
        libpcre3-dev \
        libxml2-dev \
        libxslt-dev \
        shared-mime-info \
        telnet \
        unzip \
        vim \
        wait-for-it \
        wget \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.4.1 \
    && poetry config virtualenvs.create false \
    && mkdir -p /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-interaction --no-ansi
COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
