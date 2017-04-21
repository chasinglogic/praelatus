import pytest

from praelatus.api.schemas import *  # noqa: F403
from praelatus.lib import session

import praelatus.lib.users as users
import praelatus.lib.workflows as workflows
import praelatus.lib.tickets as tickets
import praelatus.lib.permissions as permissions


@pytest.fixture
def db():
    return session()


@pytest.fixture(scope='module')
def admin():
    return users.get(session(), username='testadmin').clean_dict()


def test_signup_schema():
    SignupSchema.validate({
        "username": "some_new_user",
        "password": "supersecure",
        "full_name": "New User",
        "email": "new@praelatus.io"
    })


def test_workflow_schema(db, admin):
    workflow = workflows.get(db, actioning_user=admin, name='Default Workflow')
    WorkflowSchema.validate(workflow.clean_dict())


def test_ticket_schema(db, admin):
    """
    This test covers the following Schemas:

    TicketSchema
    UserSchema
    StatusSchema
    CommentSchema
    TicketTypeSchema
    ProjectSchema
    """
    tick = tickets.get(db, actioning_user=admin, key='TEST-10',
                       preload_comments=True)
    TicketSchema.validate(tick.clean_dict())


def test_permission_schema(db, admin):
    scheme = permissions.get(db, actioning_user=admin, id=1)
    PermissionSchemeSchema.validate(scheme.clean_dict())
