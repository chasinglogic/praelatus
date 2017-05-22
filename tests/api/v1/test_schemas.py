from praelatus.api.schemas import *  # noqa: F403

import praelatus.lib.workflows as workflows
import praelatus.lib.tickets as tickets
from praelatus.store import PermissionSchemeStore


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
    scheme = PermissionSchemeStore.get(db, actioning_user=admin, uid=1)
    PermissionSchemeSchema.validate(scheme.clean_dict())
