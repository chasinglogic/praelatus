"""Contains definition for the UserStore class."""

import bcrypt
import hashlib

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from praelatus.lib.permissions import PermissionError
from praelatus.models import User
from praelatus.models import DuplicateError
from praelatus.store.store import Store


class UserStore(Store):
    """Manages storage and retrieval of users."""

    def get(self, db, uid=None, username=None, **kwargs):
        """Get a single user, db is a SQL Alchemy session."""
        query = db.query(self.model)

        if type(uid) is int:
            query = query.filter(self.model.id == uid)
        elif type(uid) is str:
            query = query.filter(self.model.username == uid)
        elif username is not None:
            query = query.filter(self.model.username == username)
        else:
            return None

        return query.first()

    def search(self, db, search, **kwargs):
        """Search through the models and return all matches."""
        pattern = search.replace('*', '%')
        return db.query(self.model).\
            filter(
                or_(
                    self.model.username.like(pattern),
                    self.model.email.like(pattern),
                    self.model.full_name.like(pattern),
                )).\
            order_by(self.model.username).\
            all()

    def new(self, db, **kwargs):
        """Create a new user in the database then returns that user.

        The kwargs are parsed such that if a json representation of a user
        is provided as expanded kwargs it will be handled properly.

        If a required argument is not provided then it raises a KeyError
        indicating which key was missing. Useful for returning HTTP 400
        errors.

        Required Keyword Arguments:
        username -- the user name
        email -- the user's email
        password -- the user's password
        full_name -- the user's full name

        Optional Keyword Arguments:
        is_admin -- whether the user is a system admin or not (default False)
        profile_pic -- path to the user's profile picture (default Gravatar)
        """
        password = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                                 bcrypt.gensalt())
        new_user = self.model(
            username=kwargs['username'],
            password=password.decode('utf-8'),
            email=kwargs['email'],
            profile_pic=kwargs.get('profile_pic',
                                   self.gravatar(kwargs['email'])),
            is_admin=kwargs.get('is_admin', False),
            is_active=kwargs.get('is_active', True),
            full_name=kwargs['full_name']
        )

        try:
            db.add(new_user)
            db.commit()
        except IntegrityError:
            raise DuplicateError('That username is already taken.')

        return new_user

    def update(self, db, model=None, actioning_user=None):
        """Update the given user in the database.

        user must be a User class instance.
        """
        if (actioning_user is None or
            (actioning_user.get('id', 0) != model.id and
             not actioning_user.is_admin)):
            raise PermissionError('permission denied')

        db.add(model)
        db.commit()

    def delete(self, db, model=None, actioning_user=None):
        """Remove the given user from the database.

        user must be a User class instance.
        """
        if (actioning_user is None or
            (actioning_user.get('id', 0) != model.id and
             not actioning_user.is_admin)):
            raise PermissionError('permission denied')

        db.delete(model)
        db.commit()

    def gravatar(self, email):
        """Generate a gravatar profile picture link based on email."""
        md5 = hashlib.md5()
        md5.update(email.encode('utf-8'))
        return 'https://gravatar.com/avatar/' + md5.hexdigest()

    def check_pw(self, user, password):
        """Check user's password against password.

        Alias to bcrypt.checkpw.
        """
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.password.encode('utf-8'))


store = UserStore(User)
