import praelatus.lib.users as users


def test_get(db):
    user = users.get(db, username='testadmin')
    assert user is not None
    assert user.username == 'testadmin'

def test_get_with_filter(db):
    usrs = users.get(db, filter='test*')
    assert usrs is not None
    assert len(usrs) > 0
    assert usrs[0].username == 'testadmin'
