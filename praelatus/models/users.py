from base import Base
from sqlalchemy import Column, String, Integer, Boolean

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    profile_pic = Column(String)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)

    def __repr__(self):
        return "User(id=%d, username=%s)" % (self.id, self.username)
