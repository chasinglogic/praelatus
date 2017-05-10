"""Contains definition for the LabelStore class."""

from praelatus.models import Label
from praelatus.store.store import Store


class LabelStore(Store):
    """Manages storage and retrieval of labels."""
    model = Label

    def new(self, db, **kwargs):
        """Create a new label.

        This is overridden because you don't need to be a sys admin to
        create a label.
        """
        new_label = Label(name=kwargs['name'])
        db.add(new_label)
        db.commit()
