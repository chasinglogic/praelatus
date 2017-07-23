from guardian.backends import ObjectPermissionBackend
from guardian.utils import get_anonymous_user


class ObjectPermissionAnonFallbackBackend(ObjectPermissionBackend):
    """Extend ObjectPermissionBackend of to fall back to the permissions of AnonymousUser."""

    def has_perm(self, user_obj, perm, obj=None):
        """Return ``True`` if given ``user_obj`` has ``perm`` for ``obj``.

        If no ``obj`` is given, ``False`` is returned.

        .. note::
           Remember, that if user is not *active*, all checks would return
           ``False``.

        Main difference between Django's ``ModelBackend`` is that we can pass
        ``obj`` instance here and ``perm`` doesn't have to contain
        ``app_label`` as it can be retrieved from given ``obj``.

        **Inactive user support**
        If user is authenticated but inactive at the same time, all checks
        always returns ``False``.
        """
        hp = super().has_perm(user_obj, perm, obj)
        if not hp:
            return super().has_perm(get_anonymous_user(), perm, obj)
        return hp

    def get_all_permissions(self, user_obj, obj=None):
        """Return a set of permission strings that the given ``user_obj`` has for ``obj``"""
        user_perm = super().get_all_permissinos(user_obj, obj)
        anon_perm = super().get_all_permissinos(user_obj, obj)
        return user_perm + anon_perm
