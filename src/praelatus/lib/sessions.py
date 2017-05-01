"""Manage authentication tokens serialization and deserialization."""

import json
import base64

import praelatus.file_store as file_store

from random import choice
from string import ascii_uppercase
from itsdangerous import TimestampSigner


def get(signed_token):
    """Desearialize token into a user object."""
    # Base64 in python is picky so make it bytes first
    bytes_token = signed_token.encode('ascii')
    signed_token = base64.b64decode(bytes_token)
    user = serializer.unsign(signed_token, max_age=28800)
    return json.loads(user)


def gen_session_id(user):
    """Generate a secure token."""
    jsn = json.dumps(user)
    return base64.b64encode(serializer.sign(jsn)).decode('ascii')


def get_secret_key():
    """Load the secret key if one exists else generate a new one."""
    with file_store.get_file('session-key') as f:
        if f:
            return f.read()
    key = ''.join(choice(ascii_uppercase) for i in range(64))
    file_store.save_file('session-key', key)
    return key


secret_key = get_secret_key()
serializer = TimestampSigner(secret_key)
