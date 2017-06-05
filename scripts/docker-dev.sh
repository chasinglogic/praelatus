#!/bin/bash

alembic upgrade head
set -e
python scripts/seeddb.py
celery multi start -A praelatus.events &
flask run -h 0.0.0.0 -p 8000
