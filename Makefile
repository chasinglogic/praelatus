PIP="pip"

install:
	python setup.py install

build:
	python setup.py sdist bdist_wheel

.PHONY = clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
	rm -rf src/praelatus/**/__pycache__
	rm -rf src/praelatus/migrations/versions/__pycache__
