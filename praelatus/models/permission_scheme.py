from base import Base
from sqlalchemy import Column, Integer, String, relationship

class PermissionScheme(Base):
    __tablename__ = 'permission_schemes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
