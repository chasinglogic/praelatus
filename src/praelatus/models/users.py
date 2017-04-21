"""Contains definitions for the User model."""

from praelatus.models.base import Base

from sqlalchemy import Column, String, Integer, Boolean


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

    def clean_dict(self):
        """Call BaseModel clean_dict but remove password."""
        d = super(User, self).clean_dict()
        d.pop('password', None)
        return d

    def __repr__(self):
        """Override BaseModel.__repr__ for better printing."""
        return "User(id=%s, username=%s)" % (self.id, self.username)
