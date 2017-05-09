"""Contains storage classes for Praelatus."""


class Store:
    """A store manages storage of models.

    This is the base class all other stores should inherit from.
    """

    def __init__(self, model):
        """Model is the class that this store is used for."""
        self.model = model

    def get(self, db, uid=None, name=None, **kwargs):
        """Get a single model, db is a SQL Alchemy session."""
        query = db.query(self.model)

        if uid is not None:
            query = query.filter(self.model.id == uid)

        if name is not None:
            query = query.filter(self.model.name == name)

        return query.first()

    def search(self, db, search, **kwargs):
        """Search through the models and return all matches."""
        pattern = search.replace('*', '%')
        return db.query(self.model).\
            filter(self.model.name.like(pattern)).\
            order_by(self.model.name).\
            all()

    def new(self, db, **kwargs):
        """Create a new model in the database."""
        new_model = self.model(**kwargs)
        db.add(new_model)
        db.commit()

    def update(self, db, model=None, **kwargs):
        """Update the model in the database."""
        db.add(model)
        db.commit()
