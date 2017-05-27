import pytest
from praelatus.store import UserStore
from praelatus.lib import connection
import praelatus.lib.tokens as tokens
from praelatus.app import application


@pytest.fixture
def app():
    return application


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json', 'Accepts': 'application/json'}


@pytest.fixture(scope='module')
def admin():
    with connection() as db:
        return UserStore.get(db, username='testadmin').jsonify()


@pytest.fixture
def db():
    with connection() as db:
        yield db


@pytest.fixture
def auth_headers(admin, headers):
    token = tokens.gen_session_id(admin)
    headers['Authorization'] = 'Token ' + token
    return headers
