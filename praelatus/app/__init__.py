"""Entry point for gunicorn."""

import sys
from subprocess import Popen
from praelatus.app.app import app

print('Migrating database...')

alembic = Popen(['alembic', 'upgrade', 'head'])
stdout, stderr = alembic.communicate()
if stderr is not None:
    print('Error migrating database!')
    print(stderr)
    sys.exit(1)
print('Database migration finished!')

application = app
