RELEASE_FILES = app/fields app/labels app/praelatus app/profiles app/schemes app/app/data/static \
				app/templates app/tickets app/workflows LICENSE README.md app/manage.py

VERSION = 0.1.0
HASH := $(shell git rev-parse HEAD)
TARBALL = release-v$(VERSION)-$(HASH).tar.gz

WEBPACK_FILES := app/app/staticindex.js app/static/index.css

build: node_modules pip $(WEBPACK_FILES) app/data/static

clean:
	rm -rf app/data/static app/static venv/ node_modules/ $(TARBALL)

$(TARBALL): $(RELEASE_FILES)
	tar czf $@ $^

$(WEBPACK_FILES):
	npm run webpack

app/data/static:
	cd app && python manage.py collectstatic --clear

dist: build $(TARBALL)

node_modules:
	npm install

test:
	cd app && python manage.py test

run: node_modules pip
	webpack --watch & cd app && python manage.py runserver

pip: venv/lib/python3.6/site-packages/django

venv/lib/python3.6/site-packages/django:
	pip install -r app/requirements.txt

venv:
	python3 -m venv venv

activate: venv
	@echo . venv/bin/activate
