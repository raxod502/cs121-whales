.PHONY: all
all: run-server-dev

.PHONY: run-server-dev
run-server-dev:
	FLASK_APP=app/server.py FLASK_DEBUG=1 pipenv run flask run

.PHONY: run-server-prod
run-server-prod:
	pipenv run gunicorn -b "0.0.0.0:$${PORT:-5000}" --pythonpath app server:app
