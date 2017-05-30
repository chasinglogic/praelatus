PYTHON="python3"
PIP="pip"
export PYTHONPATH=${PWD}

install:
	$(PIP) install -r requirements.txt

migrate:
	alembic -c alembic.ini upgrade head

seed:
	python scripts/seeddb.py

docker_stop:
	sudo docker stop prae_postgres
	sudo docker stop prae_rabbitmq
	sudo docker stop prae_redis

docker_clean: docker_stop
	sudo docker rm prae_postgres
	sudo docker rm prae_rabbitmq
	sudo docker rm prae_redis

# Make it clean every time, otherwise step "fails"
docker_restart: docker_clean docker

docker:
	sudo docker run --name prae_postgres -d -e POSTGRES_DB=prae_dev -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
	sudo docker run --name prae_rabbitmq -d -p 5672:5672 rabbitmq
	sudo docker run --name prae_redis -d -p 6379:6379 redis

celery: docker
	celery -A praelatus.events.app worker --loglevel=debug &

run:
	FLASK_APP="praelatus.app" FLASK_DEBUG=1 PYTHONPATH=${PWD}:${PYTHONPATH} flask run -p 8000

setup_dev: install docker celery migrate seed

venv:
	$(PYTHON) -m venv venv

.PHONY = clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf praelatus/**/__pycache__
	rm -rf praelatus/migrations/versions/__pycache__
