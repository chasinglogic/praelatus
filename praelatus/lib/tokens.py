"""Manage authentication tokens serialization and deserialization."""

import json
import base64

import os

from datetime import datetime
from datetime import timedelta
from binascii import b2a_hex
from praelatus.config import config
from itsdangerous import TimestampSigner


def get_secret_key():
    """Get the secret key if exists, otherwise create a new key."""
    with open(os.path.join(config.data_dir, 'secret-key'), 'a+') as f:
        key = f.read()
        if key and key != '':
            return key
        key = b2a_hex(os.urandom(64))
        return key


s = TimestampSigner(get_secret_key())


def get(token):
    """Turn the token into the appropriate user."""
    dec = base64.b64decode(token)
    us = s.unsign(dec)
    return json.loads(us.decode('utf-8'))


# Cookies take a datetime.datetime
expires = datetime.now() + timedelta(hours=1)
# Set takes a timedelta in seconds
expires_seconds = expires - datetime.now()


def gen_session_id(user):
    """Generate a secure token."""
    jsn = json.dumps(user)
    return base64.b64encode(s.sign(jsn)).decode('utf-8')
