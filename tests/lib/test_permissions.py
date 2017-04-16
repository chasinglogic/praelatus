import praelatus.lib.permissions as permissions

def test_get(db):
    perm = permissions.get(db, name='Default Permission Scheme')
    assert perm is not None
    assert perm.name == 'Default Permission Scheme'
    assert perm.id is not None


def test_get_with_filter(db):
    perms = permissions.get(db, filter='*t*')
    assert perms is not None
    assert len(perms) > 0
    assert perms[0].id is not None

def test_update(db):
    new_name = 'Permission Scheme Default'
    perm = permissions.get(db, name='Default Permission Scheme')
    perm.name = new_name

    permissions.update(db, permission=perm)

    l = permissions.get(db, id=perm.id)
    assert l.name == new_name


def test_delete(db):
    permission = {
            'name': 'DELETE THIS',
    }

    permissions.new(db, **permission)

    l = permissions.get(db, name='DELETE THIS')
    assert l is not None

    permissions.delete(db, permission=l)

    l = permissions.get(db, name='DELETE THIS')
    assert l is None
