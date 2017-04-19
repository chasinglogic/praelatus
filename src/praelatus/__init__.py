"""
Praelatus is an Open Source bug tracking and ticketing system.

The backend API is written in Python and the frontend is a React.js
app. You are viewing the source code for the API if you would like
information about how to use the API as a client or how to start
working on the backend visit https://docs.praelatus.io
"""

from praelatus.api import create_app

__version__ = '0.0.4'
__api_version__ = 'v1'

# Global app object for gunicorn
api = create_app()
