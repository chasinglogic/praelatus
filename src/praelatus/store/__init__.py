"""Contains storage classes for Praelatus."""

from praelatus.models import Role
from praelatus.models import Field
from praelatus.models import TicketType
from praelatus.store.store import Store
from praelatus.store.users import store as UserStore
from praelatus.store.tickets import store as TicketStore  # noqa: F401
from praelatus.store.comments import store as CommentStore  # noqa: F401
from praelatus.store.permission_schemes import store as PermissionSchemeStore  # noqa: E501,F401
from praelatus.store.workflows import store as WorkflowStore  # noqa: F401
from praelatus.store.workflows import status_store as StatusStore  # noqa: F401
from praelatus.store.projects import store as ProjectStore  # noqa: F401
from praelatus.store.labels import store as LabelStore  # noqa: F401

TicketTypeStore = Store(TicketType)
RoleStore = Store(Role)
FieldStore = Store(Field)
