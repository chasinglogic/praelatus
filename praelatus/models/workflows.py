from praelatus.models.base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship


workflows_projects = Table(
    'workflows_projects', Base.metadata,
    Column('workflow_id', ForeignKey('workflows.id')),
    Column('project_id', ForeignKey('projects.id')),
    UniqueConstraint('workflow_id', 'project_id')
)


class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(Text)

    projects = relationship('Project', secondary=workflows_projects,
                            backref='worfklow')

# TODO issue #100
# class WorkflowScheme(Base):
#     __tablename__ = 'workflow_schemes'

#     id = Column(Intger, primary_key=True)
#     name = Column(String(length=255))
#     description = Column(Text)


class Transition(Base):
    __tablename__ = 'transitions'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))

    to_status_id = Column(Integer, ForeignKey('statuses.id'))
    to_status = relationship('Status', foreign_keys=to_status_id)

    from_status_id = Column(Integer, ForeignKey('statuses.id'))
    from_status = relationship('Status', foreign_keys=from_status_id)


class Hook(Base):
    __tablename__ = 'hooks'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(Text)
    body = Column(Text)
    method = Column(String(length=10))
    url = Column(String(length=255))

    transition_id = Column(Integer, ForeignKey('transitions.id'))
    transition = relationship('Transition', backref='hooks')
