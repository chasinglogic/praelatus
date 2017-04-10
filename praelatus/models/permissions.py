from praelatus.models.base import Base
from sqlalchemy import (Column, Integer, String,
                        UniqueConstraint, ForeignKey, Table)
from sqlalchemy.orm import relationship


class PermissionScheme(Base):
    __tablename__ = 'permission_schemes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class PermissionSchemePermissions(Base):
    __tablename__ = 'permission_scheme_permissions'
    __table_args__ = {
        'unique_ids': UniqueConstraint('permission_scheme_id',
                                       'role_id', 'permission_id')
        }

    id = Column(Integer, primary_key=True)
    permission_scheme_id = Column('permission_scheme_id', Integer,
                                  ForeignKey('permission_schemes.id'))
    permission_scheme = relationship('PermissionScheme',
                                     backref='permissions')

    permission_id = Column('permission_id', Integer,
                           ForeignKey('permissions.id'))
    permission = relationship('Permission')

    role_id = Column('role_id', Integer, ForeignKey('roles.id'))
    role = relationship('Role')


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserRoles(Base):
    __tablename__ = 'users_roles'
    __table_args = (
        UniqueConstraint('user_id', 'role_id', 'role_id')
        )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='roles')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', backref='roles')

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
