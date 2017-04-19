"""Contains the Base model which all models inherit from."""

import json
from sqlalchemy.ext.declarative import declarative_base


class BaseModel:
    """The Base for all models in Praelatus."""

    # This is so the __repr__ never throws AttributeError
    id = None

    def __repr__(self):
        """A basic repr method that can be inherited."""
        return "%s(id=%s)" % (self.__class__.__name__, self.id)

    def clean_dict(self):
        """
        Return a dictionary of the obj with metadata removed.

        This is used for easy jsonifying of models.
        """
        # This stores the final json obj
        jsn = {}

        for key, val in self.__dict__.items():
            # Check if it's metadata, if so skip it.
            if key.startswith("_") or key.endswith('_id'):
                continue

            # This is for FieldValue seems less hacky than deleting unused
            # values
            if key.endswith('_value'):
                continue

            # Must be a primitive type so just throw it in.
            jsn[key] = val

        return jsn

    def to_json(self):
        """A basic to_json method that works for 90% of the models."""
        # jsonify our dict using the stdlib
        return json.dumps(self.clean_dict())

    @classmethod
    def from_json(cls, jsn):
        """Inhertiable way to deserialize from json."""
        inst = cls()
        inst.__dict__ = jsn
        return inst


class DuplicateError(Exception):  # noqa: D204
    """Used for signaling to the API that an integrity rule was breached."""
    pass


Base = declarative_base(cls=BaseModel)
