# flake8: noqa

import pytest
from praelatus.lib import Session
from praelatus.seeds import seed
import praelatus.lib.users as users

@pytest.fixture(scope='module')
def admin():
    return users.get(session(), username='testadmin').clean_dict()


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    return Session()
