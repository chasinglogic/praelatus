from tickets.models import Upvote
from django import template

register = template.Library()


@register.simple_tag
def has_upvoted(user, ticket):
    q = Upvote.objects.filter(voter=user, ticket=ticket).all()
    return len(q) != 0
