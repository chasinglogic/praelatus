"""Contains storage classes for Praelatus."""

from praelatus.models import Role
from praelatus.models import Status
from praelatus.models import Field
from praelatus.models import TicketType
from praelatus.store.store import Store
from praelatus.store.tickets import TicketStore  # noqa: F401
from praelatus.store.comments import CommentStore  # noqa: F401
from praelatus.store.permission_schemes import PermissionSchemeStore  # noqa: E501,F401
from praelatus.store.workflows import WorkflowStore  # noqa: F401
from praelatus.store.projects import ProjectStore  # noqa: F401
from praelatus.store.labels import LabelStore  # noqa: F401

TicketTypeStore = Store(TicketType)
StatusStore = Store(Status)
RoleStore = Store(Role)
FieldStore = Store(Field)
