# flake8: noqa

import pytest
from praelatus.lib import session
from praelatus.store import UserStore

@pytest.fixture(scope='module')
def admin():
    with session() as db:
        return UserStore.get(db, username='testadmin').jsonify()


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    with session() as db:
        yield db
