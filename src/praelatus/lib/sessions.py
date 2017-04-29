"""Contains session management for Praelatus."""

import redis
import json
from uuid import uuid4

from praelatus.config import config


global r
r = redis.Redis(host=config.redis_host, db=config.redis_db,
                port=config.redis_port, password=config.redis_password)


def get(key):
    """Look in redis for session with key returns a User or None."""
    jsn = r.get(key)
    try:
        jsn = jsn.decode('utf-8')
        return json.loads(jsn)
    except Exception as e:
        return jsn


def set(key, val, expires=None):
    """Store the user in redis at the given session key."""
    if expires is not None:
        r.set(key, json.dumps(val), ex=expires.seconds)
        return
    r.set(key, json.dumps(val))


def delete(key):
    """Remove the value stored at key."""
    r.delete(key)


def gen_session_id():
    """Generate a secure token."""
    return uuid4()
