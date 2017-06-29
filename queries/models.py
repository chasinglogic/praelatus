from django.db import models
from django.contrib.auth.models import User

from .dsl import compile, make_q


# TODO: Maybe store the compiled query as a pickled object?
class Query(models.Model):
    """Store a query for later reference."""
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User)
    query = models.CharField(max_length=255, blank=True, null=True)

    def compile(self, make_q=make_q):
        return compile(self.query)
