"""The global flask app object."""

import flask


def create_app():
    """Create the flask application."""

    app = flask.Flask('praelatus')
    return app
