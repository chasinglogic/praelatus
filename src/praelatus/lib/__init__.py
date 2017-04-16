"""Contains all 'business logic' for Praelatus.

Any function which takes 'db' as it's first argument requires a valid
sqlachemy session.

Any function which has the kwarg 'actioning_user' is considered an
"Action" and has some security requirements, these will be handled in
the function and they default to None or "Anonymous"
"""

from praelatus.config import config
from praelatus.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_db():
    try:
        engine
    except NameError:
        global engine
        engine = create_engine(config.db_url)
        Base.metadata.create_all(engine)
        global Session
        Session = sessionmaker(bind=engine)


def session():
    try:
        return Session()
    except NameError:
        init_db()
        return Session()


def clean_db():
    init_db()
    engine.execute("DROP SCHEMA public CASCADE;")
    engine.execute("CREATE SCHEMA public;")
