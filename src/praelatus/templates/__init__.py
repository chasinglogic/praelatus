"""Functions for loading templates."""

from os.path import join
from flask import session
from flask import render_template as flask_render_template
from praelatus.config import config
from praelatus import __version__
from jinja2 import Template


def load_template(tmpl_name):
    """Load the given template.

    tmpl_name is a path relative to the template directory.
    """
    with open(join('praelatus', 'templates', tmpl_name)) as t:
        return Template(t)


def render_template(tmpl_name, **kwargs):
    """A wrapper for flask render_template that adds some of our always available variables."""
    return flask_render_template(tmpl_name, config=config,
                                 current_user=session.get('user'),
                                 prae_version=__version__,
                                 **kwargs)
