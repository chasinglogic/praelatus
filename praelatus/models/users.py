"""Contains definitions for the User model."""

from praelatus.models.base import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    """Represents a user in the database."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    profile_pic = Column(String)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)

    def jsonify(self):
        """Call BaseModel jsonify but remove password."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'profile_pic': self.profile_pic,
            'is_admin': self.is_admin,
            'is_active': self.is_active
        }

    def __repr__(self):
        """Override BaseModel.__repr__ for better printing."""
        return "User(id=%s, username=%s)" % (self.id, self.username)
