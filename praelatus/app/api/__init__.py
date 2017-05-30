"""
Contains the app factory for the flask app.

This is where error handlers are registered and routes are added.
"""

from flask import Flask
from praelatus.app.api.blueprint import api

application = Flask(__name__)
application.register_blueprint(api)
