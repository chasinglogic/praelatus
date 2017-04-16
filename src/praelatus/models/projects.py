"""Contains definitions for the Project and ProjectRoles models."""

import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from praelatus.models.base import Base
from praelatus.models.base import BaseModel


class Project(Base):
    """Defines a Project in the database."""

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    name = Column(String, unique=True)
    key = Column(String, unique=True)
    homepage = Column(String)
    icon_url = Column(String)
    repo = Column(String)

    lead_id = Column(Integer, ForeignKey('users.id'))
    lead = relationship('User', backref='lead_of')

    permission_scheme_id = Column(Integer,
                                  ForeignKey('permission_schemes.id'))
    permission_scheme = relationship('PermissionScheme', backref='projects')

    def __repr__(self):
        """Stringify the project for prettier printing."""
        return "Project(id=%d, key=%s)" % (self.id, self.key)


class ProjectRoles(BaseModel):
    """Converts UserRoles instances into the correct JSON."""

    def __init__(self, user_roles):
        """Take an array of user_roles and parse appropriately."""
        self.roles = {}
        for r in user_roles:
            self.add_role(r)
        return self

    @staticmethod
    def parse(user_role):
        """Parse out the role name and user as JSON for user_role."""
        return (user_role.role.name, user_role.user.to_json())

    def add_role(self, user_role):
        """Take a user_role parse then store in self.roles."""
        role_name, user = self.parse(user_role)
        members = self.roles.get(role_name, [])
        self.roles[role_name] = members.append(user)

    def clean_dict(self):
        """Make ProjectRoles satisfy the BaseModel if it's included."""
        return self.roles

    def to_json(self):
        """Return the json of self.roles."""
        return json.dumps(self.roles)
