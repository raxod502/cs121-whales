FROM radiansoftware/sleeping-beauty:v4.1.0 AS sleepingd

# EOL April 2031
FROM ubuntu:26.04

RUN apt-get update && apt-get install -y --no-install-recommends make python3-venv python3-poetry-plugin-export tini && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY pyproject.toml poetry.lock /src/
RUN poetry export > requirements.txt

RUN python3 -m venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:${PATH}
RUN pip3 install -r requirements.txt

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
