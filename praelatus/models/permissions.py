from praelatus.models.base import Base
from sqlalchemy import (Column, Integer, String,
                        UniqueConstraint, ForeignKey, Table)


class PermissionScheme(Base):
    __tablename__ = 'permission_schemes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


permission_scheme_permissions = Table(
    'permission_scheme_permissions', Base.metadata,
    Column('permission_scheme_id', Integer,
           ForeignKey('permission_schemes.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    UniqueConstraint('permission_scheme_id', 'role_id', 'permission_id')
)


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)


users_roles = Table(
    'users_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    UniqueConstraint('user_id', 'role_id', 'role_id')
)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
