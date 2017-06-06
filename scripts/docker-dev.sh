#!/bin/bash

alembic upgrade head
set -e
python scripts/seeddb.py
flask run -h 0.0.0.0 -p 8000
