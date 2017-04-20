"""Define the BaseSchema class."""
from jsonschema import validate


class BaseSchema():
    """Has a basic schema and inheritable validate classmethod."""

    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'}
        }
    }

    @classmethod
    def validate(cls, obj):
        """Run jsonschema validate."""
        validate(obj, cls.schema)
