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
    if jsn is None:
        return jsn
    return User.from_json(json.loads(jsn.decode('utf-8')))


def set(key, user):
    """Store the user in redis at the given session key."""
    client().set(key, user.to_json())


def gen_session_id():
    """Generated a uuid, alias for uuid.uuid4."""
    return uuid4()
