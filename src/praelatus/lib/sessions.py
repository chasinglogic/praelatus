"""Manage authentication tokens serialization and deserialization."""

import json
import base64

import praelatus.file_store as file_store

from random import SystemRandom
from itsdangerous import TimestampSigner

random = SystemRandom()


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.

    Taken from the django.utils.crypto module.
    """
    return ''.join(random.choice(allowed_chars) for i in range(length))


def generate_secret_key():
    """
    Create a random secret key.

    Taken from the Django project.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def get(signed_token):
    """Desearialize token into a user object."""
    # Base64 in python is picky so make it bytes first
    bytes_token = signed_token.encode('utf-8')
    signed_token = base64.b64decode(bytes_token)
    user = serializer.unsign(signed_token, max_age=28800)
    return json.loads(user.decode('utf-8'))


def gen_session_id(user):
    """Generate a secure token."""
    jsn = json.dumps(user)
    return base64.b64encode(serializer.sign(jsn)).decode('utf-8')


def get_secret_key():
    """Load the secret key if one exists else generate a new one."""
    with file_store.get_file('session-key') as f:
        if f:
            return f.read()
    key = generate_secret_key()
    file_store.save_file('session-key', key)
    return key


secret_key = get_secret_key()
serializer = TimestampSigner(secret_key)
