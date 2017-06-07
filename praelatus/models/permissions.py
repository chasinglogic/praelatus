"""Contains defininitions for all Permission related models."""

from enum import Enum

from praelatus.models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class PermissionScheme(Base):
    """A permission scheme ties Permissions to Roles on a Project."""
    __tablename__ = 'permission_schemes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def jsonify(self):
        """Override jsonify from BaseModel."""
        jsn = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

        permissions = {}
        for perm in self.permissions:
            perms = permissions.get(perm.role.name, [])
            perms.append(perm.permission.name)
            permissions[perm.role.name] = perms

        jsn['permissions'] = permissions
        return jsn


class PermissionSchemePermissions(Base):
    """Used to tie the Permissions for Roles to PermissionSchemes."""
    __tablename__ = 'permission_scheme_permissions'
    __table_args__ = (
        UniqueConstraint('permission_scheme_id', 'role_id',
                         'permission_id'),
    )

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
    """Used to store Permissions Enum values in the database."""
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserRoles(Base):
    """Used to tie Users to a Role for a Project."""
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
    """Used to store Roles in the database."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Permissions(Enum):
    """All of the available system permissions."""
    VIEW_PROJECT = 'VIEW_PROJECT'
    ADMIN_PROJECT = 'ADMIN_PROJECT'
    CREATE_TICKET = 'CREATE_TICKET'
    COMMENT_TICKET = 'COMMENT_TICKET'
    REMOVE_COMMENT = 'REMOVE_COMMENT'
    REMOVE_OWN = 'REMOVE_OWN_COMMENT'
    EDIT_OWN = 'EDIT_OWN_COMMENT'
    EDIT_COMMENT = 'EDIT_COMMENT'
    TRANSITION_TICKET = 'TRANSITION_TICKET'
    EDIT_TICKET = 'EDIT_TICKET'
    REMOVE_TICKET = 'REMOVE_TICKET'


class PermissionError(Exception):
    """Raised when the user doesn't have the required permission."""
    pass
