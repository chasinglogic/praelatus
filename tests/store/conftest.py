# flake8: noqa

import pytest
from praelatus.lib import connection
from praelatus.store import UserStore

@pytest.fixture(scope='module')
def admin():
    with connection() as db:
        return UserStore.get(db, username='testadmin').jsonify()


@pytest.fixture(scope='module')
def db():
    """Return a database connection as a fixture."""
    with connection() as db:
        yield db
