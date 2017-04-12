import click
from praelatus.seeds import seed
from praelatus.lib import session
from praelatus.lib import clean_db


@click.group()
def cli():
    pass


@cli.command()
def seeddb():
    db = session()
    seed(db)


@cli.command()
def cleandb():
    clean_db()


@cli.command()
def testdb():
    session()
    print("Database connection succeeded!")
