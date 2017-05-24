"""Functions for loading templates."""

from pkg_resources import resource_string
from jinja2 import Template


def load_template(tmpl_name):
    """Load the given template.

    tmpl_name is a path relative to the template directory.
    """
    body = resource_string('praelatus', 'templates/' + tmpl_name)
    return Template(body.decode('utf-8'))
