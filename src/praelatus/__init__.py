"""
Praelatus is an Open Source bug tracking and ticketing system.

The backend API is written in Python and the frontend is a React.js
app. You are viewing the source code for the API if you would like
information about how to use the API as a client or how to start
working on the backend visit https://docs.praelatus.io
"""

# Import psycopg2 appropriately based on whether we are on cpython or pypy
try:
    import psycopg2  # noqa: F401
except ImportError:
    from psycopg2cffi import compat
    compat.register()

__version__ = '0.0.4'
__api_version__ = 'v1'
