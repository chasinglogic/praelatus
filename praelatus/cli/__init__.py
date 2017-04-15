"""Contains the CLI functions for Praelatus."""

import click
import os
from os.path import dirname
from os.path import exists
from praelatus.seeds import seed
from praelatus.lib import session
from praelatus.lib import clean_db


@click.group()
def cli():  # noqa: D103
    pass


@cli.command()
def seeddb():
    """Seed the database with test data."""
    db = session()
    seed(db)


@cli.command()
def cleandb():
    """Remove all data and drop all tables from the database."""
    clean_db()


@cli.command()
def migratedb():
    """Migrate the database up to the latest version."""
    import subprocess
    from subprocess import PIPE
    alembicArgs = [
        '/bin/bash',
        'alembic',
        '-c migrations/alembic.ini',
        'upgrade',
        'head'
    ]

    if not exists('migrations/'):
        os.chdir(dirname(dirname(dirname(__file__))))

    if not exists('migrations/'):
        print("failed to find migrations,", os.getcwd())

    alembic = subprocess.Popen(alembicArgs, stdout=PIPE, stderr=PIPE,
                               cwd=os.getcwd())
    alembic.wait()


@cli.command()
def testdb():
    """Test connection to the database."""
    session()
    print("Database connection succeeded!")
