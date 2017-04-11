from praelatus.models import Label, Ticket
from praelatus.lib.utils import rollback
from sqlalchemy.orm import joinedload


def get(db, id=None, name=None, filter=None, preload_tickets=False):
    query = db.query(Label)

    if id is not None:
        query = query.filter(Label.id == id)

    if name is not None:
        query = query.filter(Label.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Label.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(Label.name).all()


@rollback
def new(db, **kwargs):
    try:
        new_label = Label(
            name=kwargs['name'],
        )
        db.add(new_label)
        db.commit()
        return new_label
    except KeyError:
        raise Exception('Missing key name')


@rollback
def update(db, label):
    db.add(label)
    db.commit()


@rollback
def delete(db, label):
    db.delete(label)
    db.commit()
