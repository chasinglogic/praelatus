# noqa: D100

import pytest
from praelatus.lib import session


@pytest.fixture(scope='module')
def db():
    """Return a database session as a fixture."""
    return session()
