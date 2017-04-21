"""Contains session management for Praelatus."""

import redis
import json

from uuid import uuid4

from praelatus.models import User
from praelatus.config import config


def __init_redis():
    """Connect to redis and set global r to connection."""
    global r
    r = redis.Redis(host=config.redis_host, db=config.redis_db,
                    port=config.redis_port, password=config.redis_password)


def client():
    """Return the global redis connection."""
    try:
        return r
    except NameError:
        __init_redis()
        return r


def get(key):
    """Look in redis for session with key returns a User or None."""
    jsn = client().get(key)
    try:
        jsn = jsn.decode('utf-8')
        return json.loads(jsn)
    except Exception as e:
        return jsn


def set(key, val, expires=None):
    """Store the user in redis at the given session key."""
    if expires is not None:
        client().set(key, json.dumps(val), ex=expires.seconds)
        return
    client().set(key, json.dumps(val))


def delete(key):
    """Remove the value stored at key."""
    client().delete(key)


def gen_session_id():
    """Generated a uuid, alias for uuid.uuid4."""
    return uuid4()
