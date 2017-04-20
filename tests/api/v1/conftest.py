import pytest
from praelatus import api


@pytest.fixture
def app():
    return api


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json', 'Accepts': 'application/json'}
