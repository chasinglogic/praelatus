PIP="pip"

.PHONY = clean
clean:
	rm -rf build
	rm -rf dist
	shopt -s globstar
	rm -rf **/__pycache__


build:
	python setup.py bdist_wheel

install:
	python setup.py install
