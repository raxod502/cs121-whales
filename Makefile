.PHONY: all
all: run-server-dev

FLASK_APP := whales.server:app

# https://stackoverflow.com/a/23569003/3538165
RUN_SERVER_PROD := gunicorn -b "0.0.0.0:$${PORT:-5000}" \
	-t 60 -w 1 --threads "$$(getconf _NPROCESSORS_ONLN)" $(FLASK_APP)

.PHONY: run-server-dev
run-server-dev: hooks
	WHALES_NO_SSL=1 FLASK_APP=$(FLASK_APP) FLASK_DEBUG=1 poetry run flask run

.PHONY: run-server-prod-test
run-server-prod-test:
	WHALES_NO_SSL=1 poetry run $(RUN_SERVER_PROD)

.PHONY: run-server-prod
run-server-prod:
	WHALES_ANALYTICS=1 $(RUN_SERVER_PROD)

.PHONY: hooks
hooks:
	@ln -sf ../../scripts/pre-commit .git/hooks/pre-commit

.PHONY: download-models
download-models:
	scripts/vendorbinaries.sh
