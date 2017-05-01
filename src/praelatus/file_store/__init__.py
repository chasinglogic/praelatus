"""An internal API for accessing and storing files.

This is so when we migrate to using S3 or supporting other forms of
storage we don't have to rewrite everything."""

import os

from praelatus.config import config
from contextlib import contextmanager


@contextmanager
def get_file(filename):
    """
    Get a file from praelatus' data directory.

    Opens read only.
    """
    if not os.path.exists(config.data_dir):
        os.mkdir(config.data_dir)

    try:
        f = open(os.path.join(config.data_dir, filename), 'r')
        yield f
        f.close()
    except:
        yield None


def save_file(filename, content):
    """
    Write to a file in praelatus' data directory.

    Always overwrites.
    """
    if not os.path.exists(config.data_dir):
        os.mkdir(config.data_dir)

    with open(os.path.join(config.data_dir, filename), 'w') as f:
        f.write(content)
