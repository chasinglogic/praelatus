# flake8: noqa

import pytest
from praelatus.lib import session
from praelatus.seeds import seed
import praelatus.lib.users as users

@pytest.fixture(scope='module')
def admin():
    with session() as db:
        return users.get(db, username='testadmin').clean_dict()


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    with session() as db:
        yield db
