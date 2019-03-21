.PHONY: all
all: run-server-dev

RUN_SERVER_PROD := pipenv run gunicorn -b "0.0.0.0:$${PORT:-5000}" --pythonpath app server:app

.PHONY: run-server-dev
run-server-dev: hooks
	WHALES_NO_SSL=1 FLASK_APP=app/server.py FLASK_DEBUG=1 pipenv run flask run

.PHONY: run-server-prod-test
run-server-prod-test:
	WHALES_NO_SSL=1 $(RUN_SERVER_PROD)

.PHONY: run-server-prod
run-server-prod:
	$(RUN_SERVER_PROD)

.PHONY: hooks
hooks:
	@ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
