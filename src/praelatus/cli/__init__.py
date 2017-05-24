"""Contains the CLI functions for Praelatus."""

import click
from os.path import join
from praelatus.lib import session
from praelatus.lib import clean_db


@click.group()
def cli():  # noqa: D103
    pass


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
    import pkg_resources

    print('Migrating the database using Alembic...')

    migrations_dir = pkg_resources.resource_filename('praelatus', 'migrations')

    alembicArgs = [
        'alembic',
        '-c',
        join(migrations_dir, 'alembic.ini'),
        'upgrade',
        'head'
    ]

    alembic = subprocess.Popen(alembicArgs,
                               cwd=pkg_resources.resource_filename('praelatus', ''))
    stdout, stderr = alembic.communicate()
    if stderr is not None:
        print(stderr)
        print('Database migration failed.')
    else:
        print('Database migration finished!')


@cli.command()
def testdb():
    """Test connection to the database."""
    session()
    print('Database connection succeeded!')


@cli.command()
@click.option("--username", default=None,
              required=True, help="Unique username")
@click.option("--passwd", default=None,
              required=True, help="Personal password")
@click.option("--fullname", default=None,
              required=True, help="User's full name")
@click.option("--email", default=None,
              required=True, help="User's email")
@click.option("--isadmin", default=False, help="Admin priviledges")
def create_user(username, passwd, fullname, email, isadmin):
    """Create a new user in the database."""
    from praelatus.store import UserStore

    nu_user = {
        'username': username,
        'password': passwd,
        'email': email,
        'full_name': fullname,
        'is_admin': isadmin,
    }

    with session() as db:
        UserStore.new(db, **nu_user)


@cli.command()
def serve():
    """Run praelatus using gunicorn and gevent.

    Not recommended for production. Please see https://doc.praelatus.io for
    production deployment options.
    """
    import os
    import subprocess
    import multiprocessing

    print("Starting praelatus...")
    host = os.getenv("PRAELATUS_HOST", "127.0.0.1")
    port = os.getenv("PRAELATUS_PORT", "8080")
    subprocess.call(["gunicorn", "-b", "%s:%s" % (host, port),
                     "-w", str(multiprocessing.cpu_count() + 1),
                     "-k", "gevent", "praelatus.api"])
