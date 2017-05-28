"""Functions for loading templates."""

from flask import session
from flask import render_template as flask_render_template
from praelatus.config import config
from praelatus import __version__
from pkg_resources import resource_string
from jinja2 import Template


def load_template(tmpl_name):
    """Load the given template.

    tmpl_name is a path relative to the template directory.
    """
    body = resource_string('praelatus', 'templates/' + tmpl_name)
    return Template(body.decode('utf-8'))


def render_template(tmpl_name, **kwargs):
    """A wrapper for flask render_template that adds some of our always available variables."""
    return flask_render_template(tmpl_name, config=config,
                                 user=session.get('user'), prae_version=__version__,
                                 **kwargs)
