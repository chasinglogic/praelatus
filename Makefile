PYTHON="python"
PIP="pip"

install:
	$(PYTHON) setup.py install

docker_stop:
	sudo docker stop prae_postgres
	sudo docker stop prae_rabbitmq
	sudo docker stop prae_redis

docker_clean: docker_stop
	sudo docker rm prae_postgres
	sudo docker rm prae_rabbitmq
	sudo docker rm prae_redis

migrate: install
	praelatus migrate

seed: migrate
	python scripts/seeddb.py

# Make it clean every time, otherwise step "fails"
docker: docker_clean
	sudo docker run --name prae_postgres -d -e POSTGRES_DB=prae_dev -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
	sudo docker run --name prae_rabbitmq -d -p 5672:5672 rabbitmq
	sudo docker run --name prae_redis -d -p 6379:6379 redis

celery: docker
	celery -A praelatus.events.app worker --loglevel=debug &

.ONESHELL:
run:
	cd src/
	PYTHONPATH=${PWD}:${PYTHONPATH} gunicorn -k gevent --reload praelatus.app

dev: install docker celery migrate seed run

build:
	$(PYTHON) setup.py sdist bdist_wheel

venv:
	$(PYTHON) -m venv venv

.PHONY = clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
	rm -rf src/praelatus/**/__pycache__
	rm -rf src/praelatus/migrations/versions/__pycache__
