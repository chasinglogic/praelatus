"""Entry point for gunicorn"""

from praelatus.app.app import create_app


application = create_app()
