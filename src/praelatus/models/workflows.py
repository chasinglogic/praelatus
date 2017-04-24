"""Contains definitions for Workflow and related models."""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from praelatus.models.base import Base


# A table that for now is just used for a 1-1 relationship see issue
# #100 for why this was created. We will eventually support "workflow"
# schemes and they will be connected through here.
workflows_projects = Table(
    'workflows_projects', Base.metadata,
    Column('workflow_id', ForeignKey('workflows.id')),
    Column('project_id', ForeignKey('projects.id')),
    UniqueConstraint('workflow_id', 'project_id')
)


class Workflow(Base):
    """Represents a Worfklow in the database."""
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(Text)

    projects = relationship('Project',
                            secondary=workflows_projects,
                            back_populates='workflows')

    def clean_dict(self):
        """Override BaseModel clean_dict."""
        jsn = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

        transitions = {}
        for tr in self.transitions:
            from_status = ''
            # If there is no from_status that means that it's the "Create" step
            if tr.from_status is None:
                from_status = 'Create'
            else:
                from_status = tr.from_status.name

            ts = transitions.get(from_status, [])
            ts.append(tr.clean_dict())

            transitions[from_status] = ts

        jsn['transitions'] = transitions
        return jsn


# TODO issue #100
# class WorkflowScheme(Base):
#     __tablename__ = 'workflow_schemes'

#     id = Column(Intger, primary_key=True)
#     name = Column(String(length=255))
#     description = Column(Text)


class Transition(Base):
    """Represents a workflow Transition in the database."""
    __tablename__ = 'transitions'
    __table_args__ = (
        UniqueConstraint('name', 'workflow_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))

    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    workflow = relationship('Workflow', backref='transitions')

    to_status_id = Column(Integer, ForeignKey('statuses.id'))
    to_status = relationship('Status', foreign_keys=to_status_id)

    from_status_id = Column(Integer, ForeignKey('statuses.id'))
    from_status = relationship('Status', foreign_keys=from_status_id)

    def clean_dict(self):
        """Override BaseModel clean_dict."""
        jsn = super(Transition, self).clean_dict()
        jsn['to_status'] = self.to_status.clean_dict()
        jsn['hooks'] = []
        for h in self.hooks:
            jsn['hooks'].append(h.clean_dict())
        jsn.pop('from_status', None)
        return jsn


class Hook(Base):
    """Represents a hook for a Transition in the database."""
    __tablename__ = 'hooks'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(Text)
    body = Column(Text)
    method = Column(String(length=10))
    url = Column(String(length=255))

    transition_id = Column(Integer, ForeignKey('transitions.id'))
    transition = relationship('Transition', backref='hooks')
