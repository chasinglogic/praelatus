"""Contains definition for the ProjectStore class."""

from sqlalchemy import or_

from praelatus.models import Project
from praelatus.models import User
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import add_permission_query
from praelatus.store.store import Store


class ProjectStore(Store):
    """Stores and retrieves Projects."""
    model = Project

    def get(self, db, uid=None, id=None, name=None,
            actioning_user=None, **kwargs):
        """Get a single project from the database."""
        query = db.query(Project)
        query = add_permission_query(db, query,
                                     actioning_user, 'VIEW_PROJECT')
        if uid is not None:
            query = query.filter(Project.key == uid)
        elif id is not None:
            query = query.filter(Project.id == id)
        elif name is not None:
            query = query.filter(Project.name == name)
        else:
            return None
        return query.first()

    def search(self, db, search, actioning_user=None, **kwargs):
        """Search through projects and return all matches."""
        pattern = filter.replace('*', '%')
        query = db.query(Project).filter(
            or_(
                Project.name.like(pattern),
                Project.key.like(pattern),
                User.username.like(pattern),
                User.full_name.like(pattern)
            )
        )

        query = add_permission_query(db, query, actioning_user, 'VIEW_PROJECT')
        return query.order_by(Project.key).all()

    @permission_required('ADMIN_PROJECT')
    def update(self, db, model=None, **kwargs):
        """Update the project in the database."""
        db.add(model)
        db.commit()

    @permission_required('ADMIN_PROJECT')
    def delete(self, db, model=None, **kwargs):
        """Update the project in the database."""
        db.delete(model)
        db.commit()
