# EOL April 2027
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

COPY pyproject.toml poetry.lock /src/
RUN poetry install

COPY Makefile /src/
COPY whales/ /src/whales/

CMD exec make run-server-prod
