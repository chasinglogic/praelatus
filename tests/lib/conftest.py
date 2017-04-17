# flake8: noqa

import pytest
from praelatus.lib import session
from praelatus.seeds import seed
import praelatus.lib.users as users

@pytest.fixture(scope='module')
def admin():
    return users.get(session(), username='testadmin')


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    return session()
