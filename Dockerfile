FROM radiansoftware/sleeping-beauty:v4.1.0 AS sleepingd

# EOL April 2027
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl python3 python3-pip tini && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

COPY pyproject.toml poetry.lock /src/
RUN poetry install

COPY Makefile /src/
COPY whales/ /src/whales/

COPY --from=sleepingd /sleepingd /usr/local/bin/sleepingd
ENTRYPOINT ["/usr/bin/tini", "--"]

ENV SLEEPING_BEAUTY_COMMAND="make run-server-prod PORT=5001"
ENV SLEEPING_BEAUTY_TIMEOUT_SECONDS=300
ENV SLEEPING_BEAUTY_COMMAND_PORT=5001
ENV SLEEPING_BEAUTY_LISTEN_PORT=5000

CMD ["sleepingd"]
EXPOSE 5000
