PIP="pip"

install:
	python setup.py install

build:
	python setup.py sdist bdist_wheel

.PHONY = clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf **/__pycache__
	rm -rf **/*.egg-info
