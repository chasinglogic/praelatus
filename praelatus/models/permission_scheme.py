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


users_roles = Table('users_roles', Base.metadata,
                    Column('user_id', Integer,
                           ForeignKey('users.id')),
                    Column('project_id', Integer,
                           ForeignKey('projects.id')),
                    Column('role_id', Integer,
                           ForeignKey('roles.id'))
)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
