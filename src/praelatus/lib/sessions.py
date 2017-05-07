"""Contains session management for Praelatus."""

import json
import os
import base64

from datetime import datetime
from datetime import timedelta
from binascii import b2a_hex
from itsdangerous import TimestampSigner
from praelatus.config import config


def get_secret_key():
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
    signed = s.sign(json.dumps(user))
    return base64.b64encode(signed).decode('ascii')
