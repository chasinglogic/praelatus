#!/bin/bash

until python manage.py migrate; do
    echo "Postgres not up yet waiting..."
    sleep 2
done

python manage.py loaddata fixtures.json &

echo "Starting praelatus..."
python manage.py runserver 0.0.0.0:8000
