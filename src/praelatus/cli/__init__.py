"""Contains the CLI functions for Praelatus."""

import click
from os.path import dirname
from os.path import exists
from os.path import join
from praelatus.seeds import seed
from praelatus.lib import session
from praelatus.lib import clean_db


@click.group()
def cli():  # noqa: D103
    pass


@cli.command()
def seeddb():
    """Seed the database with test data."""
    print("Seeding the database with test data."
          "This may take a minute...")
    seed()
    print("Seeding finished.")


@cli.command()
@click.option('--yes', is_flag=True)
def cleandb(yes):
    """Remove all data and drop all tables from the database."""
    print('WARNING: This will remove ALL data and tables from the database.')
    print('This operation is irreversible.')
    if not yes:
        answer = input('Are you sure? y/N: ')
    if yes or 'y' in answer.lower():
        clean_db()
        print('All data removed.')
    else:
        print('No data was removed.')


@cli.command()
def migrate():
    """Migrate the database up to the latest version."""
    import subprocess

    print('Migrating the database using Alembic...')

    migrations_dir = dirname(dirname(dirname(__file__))).replace(' ', '')
    print(migrations_dir)

    alembicArgs = [
        'alembic',
        '-c',
        '%s' % join(migrations_dir, 'migrations', 'alembic.ini'),
        'upgrade',
        'head'
    ]

    if not exists(migrations_dir):
        print('failed to find migrations,', migrations_dir)
        return

    alembic = subprocess.Popen(alembicArgs, cwd=migrations_dir)
    stdout, stderr = alembic.communicate()
    if stderr is not None:
        print(stderr)
        print('Database migration failed.')
    else:
        print('Database migration finished!')


@cli.command()
def test():
    """Test connection to the database."""
    session()
    print('Database connection succeeded!')
