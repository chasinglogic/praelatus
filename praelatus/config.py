"""Contains all of the configuration for Praelatus"""
import json
import os


def init():
    global config
    config = {}

    if os.path.exists('./config.json'):
        config = json.loads('./config.json')
        return

    config['DB_URL'] = os.getenv('PRAELATUS_DB')
    if config['DB_URL'] is None:
        config['DB_URL'] = 'postgres://postgres:postgres@localhost:5432/prae_dev'

    config['PORT'] = os.getenv('PRAELATUS_PORT')
    if config['PORT'] is None:
        config['PORT'] = '8080'

    return


try:
    config
except NameError:
    init()
