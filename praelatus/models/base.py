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

    def get(self, attr):
        """Works like dict .get."""
        return getattr(self, attr)

    def jsonify(self):
        """
        Return a dictionary of the obj with metadata removed.

        This is used for easy jsonifying of models.
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def to_json(self):
        """A basic to_json method that works for 90% of the models."""
        # jsonify our dict using the stdlib
        return json.dumps(self.jsonify())

    @classmethod
    def from_json(cls, jsn):
        """Inhertiable way to deserialize from json."""
        inst = cls()
        inst.__dict__ = jsn
        return inst

    def update_from_json(self, jsn):
        """Inheritable way to update a class instance from json."""
        self.__dict__.update(jsn)


class DuplicateError(Exception):  # noqa: D204
    """Used for signaling to the API that an integrity rule was breached."""
    pass


Base = declarative_base(cls=BaseModel)
