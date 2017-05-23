"""Contains definition for the LabelStore class.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from praelatus.models import Label
from praelatus.store.store import Store


class LabelStore(Store):
    """Manages storage and retrieval of labels."""

    def new(self, db, **kwargs):
        """Create a new label.

        This is overridden because you don't need to be a sys admin to
        create a label.
        """
        new_label = Label(name=kwargs['name'])
        db.add(new_label)
        db.commit()

        return new_label


store = LabelStore(Label)
