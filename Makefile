RELEASE_FILES = fields labels praelatus profiles schemes data/static \
				templates tickets workflows LICENSE README.md manage.py

VERSION = 0.1.0
HASH := $(shell git rev-parse HEAD)
TARBALL = release-v$(VERSION)-$(HASH).tar.gz

WEBPACK_FILES := static/index.js static/index.css

build: install_deps $(WEBPACK_FILES) data/static

clean:
	rm -rf data/static static/ venv/ node_modules/ $(TARBALL)

$(TARBALL): $(RELEASE_FILES)
	tar czf $@ $^

$(WEBPACK_FILES):
	webpack

data/static:
	python manage.py collectstatic --clear

dist: build $(TARBALL)

node_modules:
	npm install

install_deps: node_modules pip

test:
	python manage.py test

run: node_modules pip
	webpack --watch & python manage.py runserver

pip: .venv/lib/python3.6/django

.venv/lib/python3.6/django:
	pip install -r requirements.txt

.venv:
	python3 -m venv .venv

venv: .venv
activate:
	@echo . .venv/bin/activate
