"""
An internal API for accessing and storing files.

This is so when we can transparently support using S3 or supporting
other forms of storage we don't have to rewrite everything.
"""

import os

from praelatus.config import config


def get_file(filename):
    """
    Get the contents of filename and return them.

    Opens read only.
    """
    if not os.path.exists(config.data_dir):
        os.mkdir(config.data_dir)

    try:
        fp = os.path.join(config.data_dir, filename)
        with open(fp, 'r') as f:
            return f.read()
    except:
        return None


def save_file(filename, content):
    """
    Write to a file in praelatus' data directory.

    Always overwrites.
    """
    if not os.path.exists(config.data_dir):
        os.mkdir(config.data_dir)

    with open(os.path.join(config.data_dir, filename), 'w') as f:
        f.write(content)
