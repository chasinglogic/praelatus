from django.db import models
from django.contrib.auth.models import User

from .dsl import compile_q, make_q


# TODO: Maybe store the compiled query as a pickled object?
class Query(models.Model):
    """Store a query for later reference."""
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User)
    query = models.CharField(max_length=255, blank=True, null=True)
    favorite = models.BooleanField(default=False)

    def compile(self, make_q=make_q):
        return compile_q(self.query)

    @classmethod
    def favorites(cls, user):
        """Get the favorite queries for the given user."""
        return cls.objects.filter(favorite=True, owner=user)

    class Meta:
        unique_together = (('owner', 'name'),)


class QueryUse(models.Model):
    """Store recently used queries."""
    user = models.ForeignKey(User)
    query = models.ForeignKey(Query)
    last_used = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'query'),)
