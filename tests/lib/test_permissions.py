import praelatus.lib.permissions as permissions
import praelatus.seeds.defaults as defaults
import praelatus.lib.users as users

def test_get(db, admin):
    perm = permissions.get(db, actioning_user=admin,
                           name='Default Permission Scheme')
    assert perm is not None
    assert perm.name == 'Default Permission Scheme'
    assert perm.id is not None


def test_get_with_filter(db, admin):
    perms = permissions.get(db, actioning_user=admin, filter='*e*')
    assert perms is not None
    assert len(perms) > 0
    assert perms[0].id is not None


def test_update(db, admin):
    new_name = 'Permission Scheme Default'
    perm = permissions.get(db, actioning_user=admin,
                           name='Default Permission Scheme')
    perm.name = new_name

    permissions.update(db, actioning_user=admin,
                       permission_scheme=perm)

    l = permissions.get(db, actioning_user=admin, id=perm.id)
    assert l.name == new_name


def test_delete(db, admin):
    permission = defaults.permission_scheme
    permission['name'] = 'DELETE THIS'

    permissions.new(db, actioning_user=admin, **permission)

    s = permissions.get(db, actioning_user=admin, name='DELETE THIS')
    assert s is not None

    permissions.delete(db, actioning_user=admin, permission_scheme=s)

    s = permissions.get(db, actioning_user=admin, name='DELETE THIS')
    assert s is None


def test_is_system_admin(db, admin):
    assert permissions.is_system_admin(db, admin) is True
    user = users.get(db, username='testuser')
    assert permissions.is_system_admin(db, user) is False



def test_json(db, admin):
    json_scheme = {
        'name':        'JSON Permission Scheme',
        'description': 'A test for JSON Serialization.',
        'permissions': {
            'Administrator': [
                'VIEW_PROJECT',
                'ADMIN_PROJECT',
                'CREATE_TICKET',
                'COMMENT_TICKET',
                'REMOVE_COMMENT',
                'REMOVE_OWN_COMMENT',
                'EDIT_OWN_COMMENT',
                'EDIT_COMMENT',
                'TRANSITION_TICKET',
                'EDIT_TICKET',
                'REMOVE_TICKET',
            ],
            'Contributor': [
                'VIEW_PROJECT',
                'CREATE_TICKET',
                'COMMENT_TICKET',
                'REMOVE_OWN_COMMENT',
                'EDIT_OWN_COMMENT',
                'TRANSITION_TICKET',
                'EDIT_TICKET',
            ],
            'User': [
                'VIEW_PROJECT',
                'CREATE_TICKET',
                'COMMENT_TICKET',
                'REMOVE_OWN_COMMENT',
                'EDIT_OWN_COMMENT',
            ],
            'Anonymous': [
                'VIEW_PROJECT',
            ],
        }
    }

    j = permissions.new(db, actioning_user=admin, **json_scheme)
    json_scheme['id'] = j.id
    assert j.clean_dict() == json_scheme
