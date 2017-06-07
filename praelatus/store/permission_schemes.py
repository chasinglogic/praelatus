"""Contains definition for the PermissionSchemeStore."""

from praelatus.lib.permissions import sys_admin_required
from praelatus.models import (Permission, PermissionScheme,
                              PermissionSchemePermissions, Role)
from praelatus.store import Store


class PermissionSchemeStore(Store):
    """Stores and retrieves permission schemes."""

    @sys_admin_required
    def get(self, db, uid=None, name=None, **kwargs):
        """Get a Permission Scheme."""
        return super(PermissionSchemeStore, self).\
            get(db, uid=uid, name=name, **kwargs)

    @sys_admin_required
    def search(self, db, search, **kwargs):
        """Search Permission Schemes."""
        return super(PermissionSchemeStore, self).\
            search(db, search, **kwargs)

    @sys_admin_required
    def new(self, db, **kwargs):
        """Add permission scheme to if acitoning_user has permission.

        Required Keyword Arguments:
        """
        new_scheme = PermissionScheme(
            name=kwargs['name'],
            description=kwargs.get('description', '')
        )

        permissions = kwargs['permissions']
        for role_name, perms in permissions.items():
            role = db.query(Role).filter_by(name=role_name).first()
            for perm in perms:
                permission = db.query(Permission).filter_by(name=perm).first()
                perm_scheme_perm = PermissionSchemePermissions(
                    role_id=role.id,
                    permission_id=permission.id
                )

                new_scheme.permissions.append(perm_scheme_perm)

        db.add(new_scheme)
        db.commit()

        return new_scheme


store = PermissionSchemeStore(PermissionScheme)
