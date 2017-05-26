PYTHON="python"
PIP="pip"

install:
	$(PYTHON) setup.py install

.ONESHELL:
dev:
	cd src/
	PYTHONPATH=${PWD}:${PYTHONPATH} gunicorn -k gevent --reload praelatus.app

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
