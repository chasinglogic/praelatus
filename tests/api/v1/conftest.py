import pytest
import praelatus.lib.users as users
from praelatus.lib import session
import praelatus.lib.sessions as sessions
from praelatus.api import application


@pytest.fixture
def app():
    return application


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json', 'Accepts': 'application/json'}


@pytest.fixture(scope='module')
def admin():
    with session() as db:
        return users.get(db, username='testadmin').clean_dict()


@pytest.fixture
def db():
    with session() as db:
        yield db


@pytest.fixture
def auth_headers(admin, headers):
    token = sessions.gen_session_id()
    sessions.set(token, admin)
    headers['Authorization'] = 'Token ' + str(token)
    return headers
