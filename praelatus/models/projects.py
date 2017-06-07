"""Contains definitions for the Project and ProjectRoles models."""

import json
from datetime import datetime

from praelatus.models.base import Base, BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Project(Base):
    """Defines a Project in the database."""

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    name = Column(String, unique=True)
    key = Column(String, unique=True)
    description = Column(String)
    homepage = Column(String)
    icon_url = Column(String)
    repo = Column(String)

    lead_id = Column(Integer, ForeignKey('users.id'))
    lead = relationship('User', backref='lead_of')

    permission_scheme_id = Column(Integer,
                                  ForeignKey('permission_schemes.id'))
    permission_scheme = relationship('PermissionScheme', backref='projects')

    workflows = relationship('Workflow', back_populates='projects',
                             secondary='workflows_projects')

    def jsonify(self):
        """Override BaseModel jsonify."""
        return {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'description': self.description,
            'homepage': self.homepage,
            'icon_url': self.icon_url,
            'repo': self.repo,
            'lead': self.lead.jsonify(),
            'created_date': str(self.created_date)
        }

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

    def jsonify(self):
        """Make ProjectRoles satisfy the BaseModel if it's included."""
        return self.roles

    def to_json(self):
        """Return the json of self.roles."""
        return json.dumps(self.roles)
