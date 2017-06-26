import markdown as md
from django import template

register = template.Library()


@register.filter
def markdown(text):
    # safe_mode governs how the function handles raw HTML
    return md.markdown(text, safe_mode='escape')
