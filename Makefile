RELEASE_FILES =  static templates praelatus apps LICENSE README.md manage.py

VERSION = 0.1.0
HASH := $(shell git rev-parse HEAD)
TARBALL = release-v$(VERSION)-$(HASH).tar.gz

WEBPACK_FILES := static/index.js static/index.css

build: node_modules pip $(WEBPACK_FILES) data/static

clean:
	rm -rf data/static static venv/ node_modules/ $(TARBALL)

$(TARBALL): $(RELEASE_FILES)
	tar czf $@ $^

$(WEBPACK_FILES):
	npm run build

data/static:
	python manage.py collectstatic --clear

dist: build $(TARBALL)

node_modules:
	npm install

test:
	python manage.py test

run: 
	npm run dev & PRAE_DEBUG=true python manage.py runserver

pip: venv/lib/python3.6/site-packages/django

.venv/lib/python3.6/site-packages/django:
	pip install -r requirements.txt

.venv:
	python3 -m venv .venv

activate: venv
	@echo . venv/bin/activate

migrate:
	python manage.py makemigrations && python manage.py migrate

seeddb: migrate
	python manage.py flush && python manage.py seeddb
