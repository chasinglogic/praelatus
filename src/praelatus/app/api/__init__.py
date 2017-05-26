"""
Contains the app factory for the falcon.API.

This is where error handlers are registered and routes are added.
"""

from praelatus.app.api.v1 import add_v1_routes


def add_api_routes(app):
    """Factory method for our API."""
    add_v1_routes(app)
    # Make v1 the 'latest' api version
    add_v1_routes(app, prefix='/api/')
