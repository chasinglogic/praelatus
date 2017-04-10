import praelatus.lib.users as users
import pytest
from praelatus.lib import session


@pytest.fixture
def db():
    return session()


def test_new_and_get(db):
    # users.new(
    #     db,
    #     username='testadmin',
    #     password='test',
    #     email='test@example.com',
    #     is_admin=True,
    #     full_name='Test Testerson'
    # )

    user = users.get(db, username='testadmin')
    assert user is not None
    assert user.username == 'testadmin'

    usrs = users.get(db, filter='test*')
    assert usrs is not None
    assert len(usrs) > 0
    assert usrs[0].username == 'testadmin'
