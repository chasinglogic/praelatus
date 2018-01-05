RELEASE_FILES = fields labels praelatus profiles schemes data/static templates tickets workflows LICENSE README.md manage.py

VERSION = 0.1.0
HASH := $(shell git rev-parse HEAD)
TARBALL = release-v$(VERSION)-$(HASH).tar.gz

WEBPACK_FILES := static/index.js static/index.css

build: install_deps $(WEBPACK_FILES) data/static

clean:
	rm $(TARBALL)
	rm -rf data/static static/ venv/

$(TARBALL): $(RELEASE_FILES)
	tar czf $@ $^

$(WEBPACK_FILES):
	webpack

data/static:
	. .venv/bin/activate && python manage.py collectstatic --clear

dist: build $(TARBALL)

node_modules:
	npm install

install_deps: node_modules pip

test:
	. .venv/bin/activate && python manage.py test

run:
	webpack --watch & . .venv/bin/activate && python manage.py runserver

pip: .venv .venv/lib/python3.6/django

.venv/lib/python3.6/django:
	. .venv/bin/activate && pip install -r requirements.txt

.venv:
	python3 -m venv .venv
