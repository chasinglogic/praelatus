import praelatus.lib.users as users

from praelatus.api.schemas import SignupSchema
from praelatus.api.schemas import UserSchema


def test_get(db):
    user = users.get(db, username='testadmin')
    assert user is not None
    assert user.username == 'testadmin'


def test_get_with_filter(db):
    usrs = users.get(db, filter='test*')
    assert usrs is not None
    assert len(usrs) > 0
    assert usrs[0].username == 'testadmin'


def test_delete(db):
    users.new(db, **{
        'username': 'delete_me',
        'password': 'none',
        'email': 'delete_me@delete.com',
        'full_name': 'DELETE ME',
        'is_active': True,
    })

    # verify we can retreieve the user
    u = users.get(db, username='delete_me')
    assert u is not None

    users.delete(db, u, actioning_user=u)

    u = users.get(db, username='delete_me')
    assert u is None


def test_update(db):
    email = 'anonmyous@example.com'
    anon = users.get(db, id=1)

    anon.email = email

    users.update(db, anon, actioning_user=anon)

    a = users.get(db, id=1)
    assert a is not None
    assert a.email == email


def test_gravatar():
    gravatar = 'https://gravatar.com/avatar/9cd743073d56a5958655e3cf2105728b'
    assert gravatar == users.gravatar('chasinglogic@gmail.com')


def test_check_pw(admin):
    assert users.check_pw(admin, 'test')


def test_user_schema(admin):
    UserSchema.validate(admin.clean_dict())


def test_signup_schema():
    SignupSchema.validate({
        "username": "some_new_user",
        "password": "supersecure",
        "full_name": "New User",
        "email": "new@praelatus.io"
    })
