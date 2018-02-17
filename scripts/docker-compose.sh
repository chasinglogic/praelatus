#!/bin/bash

source /opt/venv/bin/activate

export PRAE_DEBUG="true"

echo "Migrating database..."
until python manage.py migrate; do
    echo "Migrating database finished $?..."
done

echo "Seeding database..."
until python manage.py seeddb; do
    echo "Seeding database finished $?..."
done

echo "Starting app.."
until gunicorn -b 0.0.0.0:8000 \
         --reload \
         -k gevent \
	     --worker-connections 1000 \
	     -w 1 \
         $@ \
	     praelatus.wsgi; do
    echo "App crashed restarting..."
    sleep 1
done