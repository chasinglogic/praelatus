from praelatus.models import Field
from praelatus.models import FieldOption
from praelatus.models.fields import DATA_TYPES
from praelatus.lib.utils import rollback


def get(db, id=None, name=None, filter=None):
    query = db.query(Field)

    if id is not None:
        query = query.filter(Field.id == id)

    if name is not None:
        query = query.filter(Field.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Field.name.like(pattern))

    if any([id, name]):
        return query.first()
    return query.order_by(Field.name).all()


def valid_type(data_type):
    """Raise an exception if data_type isn't in the accepted DATA_TYPES."""
    if data_type in DATA_TYPES:
        return data_type
    raise Exception('Invalid data type %s please select from %s' %
                    (data_type, DATA_TYPES))


@rollback
def new(db, **kwargs):
    try:
        new_field = Field(
            name=kwargs['name'],
            data_type=valid_type(kwargs['data_type']),
        )

        options = kwargs.get('options', [])
        for o in options:
            new_field.options.append(FieldOption(name=o['name']))

        db.add(new_field)
        db.commit()
        return new_field
    except KeyError as e:
        raise Exception('Missing key ' + e.args[0])


@rollback
def update(db, field):
    db.add(field)
    db.commit()


@rollback
def delete(db, field):
    db.delete(field)
    db.commit()
