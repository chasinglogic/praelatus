# flake8: noqa

import pytest
from praelatus.lib import session
from praelatus.seeds import seed
import praelatus.lib.users as users

global seeded
seeded = False

@pytest.fixture(scope='module')
def admin():
    return users.get(session(), username='testadmin')


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    sess = session()

    if not seeded:
        seed(sess)
        global seeded
        seeded = True

    return session()
