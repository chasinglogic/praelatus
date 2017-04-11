"""Contains functions for interacting with users."""
import bcrypt
import hashlib
from praelatus.lib.utils import rollback
from praelatus.models.users import User


def get(db, username=None, id=None, email=None, filter=None):
    query = db.query(User)

    if username is not None:
        query = query.filter(User.username == username)

    if id is not None:
        query = query.filter(User.id == id)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(User.username.like(pattern))

    if any([username, id, email]):
        return query.first()
    return query.order_by(User.username).all()


@rollback
def new(db, **kwargs):
    try:
        password = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                                 bcrypt.gensalt())
        new_user = User(
            username=kwargs['username'],
            password=password,
            email=kwargs['email'],
            profile_pic=gravatar(kwargs['email']),
            is_admin=kwargs.get('is_admin', False),
            is_active=kwargs.get('is_active', True),
            full_name=kwargs['full_name'])
        db.add(new_user)
        db.commit()
        return new_user
    except KeyError as e:
        raise Exception('Missing key' + str(e.args[0]))


@rollback
def update(db, user, actioning_user=None):
    if (actioning_user is None
        or (actioning_user.id != user.id
            and not actioning_user.is_admin)):
        raise Exception('permission denied')

    db.add(user)
    db.commit()


@rollback
def delete(db, user, actioning_user=None):
    if (actioning_user is None
        or (actioning_user.id != user.id
            and not actioning_user.is_admin)):
        raise Exception('permission denied')

    db.delete(user)
    db.commit()


def gravatar(email):
    md5 = hashlib.md5()
    md5.update(email.encode('utf-8'))
    return md5.digest()
