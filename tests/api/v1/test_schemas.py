from praelatus.api.schemas import *  # noqa: F403

from praelatus.store import PermissionSchemeStore
from praelatus.store import TicketStore
from praelatus.store import WorkflowStore


def test_signup_schema():
    SignupSchema.validate({
        "username": "some_new_user",
        "password": "supersecure",
        "full_name": "New User",
        "email": "new@praelatus.io"
    })


def test_workflow_schema(db, admin):
    workflow = WorkflowStore.get(db, actioning_user=admin, name='Default Workflow')
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
    tick = TicketStore.get(db, actioning_user=admin, uid='TEST-10',
                           preload_comments=True)
    TicketSchema.validate(tick.clean_dict())


def test_permission_schema(db, admin):
    scheme = PermissionSchemeStore.get(db, actioning_user=admin, uid=1)
    PermissionSchemeSchema.validate(scheme.clean_dict())
