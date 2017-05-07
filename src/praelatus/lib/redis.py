"""Contains session management for Praelatus."""

import redis
import logging
import json

from functools import wraps
from praelatus.config import config


global r
r = redis.Redis(host=config.redis_host, db=config.redis_db,
                port=config.redis_port, password=config.redis_password)


def cached(fn):
    """Back this lib method with a caching mechanism."""
    @wraps(fn)
    def cached_db(*args, **kwargs):
        cached = None
        if kwargs.get('id'):
            cached = r.get(kwargs['id'])
        elif kwargs.get('key'):
            cached = r.get(kwargs['key'])

        if cached and kwargs.get('cached'):
            return json.loads(cached.decode('utf-8'))

        res = fn(*args, **kwargs)
        if type(res) is list:
            return res
        elif getattr(res.__class__, 'key'):
            r.set(res.key, res.to_json())
        else:
            r.set(res.id, res.to_json())

        return res

    return cached_db
