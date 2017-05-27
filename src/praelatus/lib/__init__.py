"""
Contains all 'business logic' for Praelatus.

Any function which takes 'db' as it's first argument requires a valid
sqlachemy session.

Any function which has the kwarg 'actioning_user' is considered an
"Action" and has some security requirements, these will be handled in
the function and they default to None or "Anonymous"
"""

import sys
import traceback

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from praelatus.config import config

global engine
engine = create_engine(config.db_url)

global Session
Session = sessionmaker(bind=engine)


@contextmanager
def connection():
    """Return a session to for the database will connect if not connected."""
    connection = Session()
    try:
        yield connection
    except Exception as e:
        _, _, stack = sys.exc_info()
        traceback.format_tb(stack)
        connection.rollback()
        raise e
    finally:
        connection.close()


def clean_db():
    """Remove all tables and data from the database."""
    engine.execute("DROP SCHEMA public CASCADE;")
    engine.execute("CREATE SCHEMA public;")
