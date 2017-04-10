import praelatus.lib.users as users
import praelatus.lib.projects as projects
import pytest
from praelatus.lib import session


@pytest.fixture
def db():
    return session()


def test_get_one(db):
    project = projects.get(db, key='TEST')
    assert project is not None
    assert project.key == 'TEST'


def test_get_filter(db):
    pjs = projects.get(db, filter='test*')
    print(pjs)
    assert pjs is not None
    assert len(pjs) > 0
    assert pjs[0].key == 'TEST'


def test_get_filter_action(db):
    admin = users.get(db, username='testadmin')

    pjs = projects.get(db, filter='test*', actioning_user=admin)
    print(pjs)
    assert pjs is not None
    assert len(pjs) > 0
    assert pjs[0].key == 'TEST'
