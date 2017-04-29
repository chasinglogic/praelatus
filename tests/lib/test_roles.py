import praelatus.lib.roles as roles
import praelatus.seeds.defaults as defaults
import praelatus.lib.users as users


def test_get(db, admin):
    role = roles.get(db, actioning_user=admin,
                           name='Administrator')
    assert role is not None
    assert role.name == 'Administrator'
    assert role.id is not None


def test_get_with_filter(db, admin):
    rles = roles.get(db, actioning_user=admin, filter='*e*')
    assert rles is not None
    assert len(rles) > 0
    assert rles[0].id is not None


def test_update(db, admin):
    new_name = 'Viewer'
    role = roles.get(db, actioning_user=admin,
                           name='User')
    role.name = new_name

    roles.update(db, actioning_user=admin, role=role)

    l = roles.get(db, actioning_user=admin, id=role.id)
    assert l.name == new_name


def test_delete(db, admin):
    role = {
        'name': 'DELETE THIS'
    }

    roles.new(db, actioning_user=admin, **role)

    s = roles.get(db, actioning_user=admin, name='DELETE THIS')
    assert s is not None

    roles.delete(db, actioning_user=admin, role=s)

    s = roles.get(db, actioning_user=admin, name='DELETE THIS')
    assert s is None

