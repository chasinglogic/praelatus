"""Contains all of the configuration for Praelatus."""

import json
import os


class Config:
    """Contains all global app configuration and defaults."""

    db = 'postgres://postgres:postgres@localhost:5432/prae_dev'
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    port = '8080'
    data_dir = './data'
    data_dir = './data/'
    mq_server = 'amqp://guest@localhost'
    smtp_server = 'localhost'
    smtp_password = None
    email_address = 'praelatus@localhost'
    instance_name = 'Praelatus, An Open Source Bug Tracker and Ticketing System'

    def __repr__(self):
        """Return the str version of the internal dict."""
        return str(self.__dict__)

    def to_json(self):
        """Serialize the config to json."""
        return json.dumps(self.__dict__)

    def load(self):
        """Create a new Config based on the config file or environment variables."""  # noqa: E501
        c = Config()

        if os.path.exists('/etc/praelatus/config.json'):
            config = json.loads('/etc/praelatus/config.json')
            c.__dict__ = config
            return c

        if os.path.exists('./config.json'):
            config = json.loads('./config.json')
            c.__dict__ = config
            return c

        c.db = os.environ.get('PRAELATUS_DB', c.db)
        c.port = os.environ.get('PRAELATUS_PORT', c.port)
        c.redis_host = os.getenv('PRAELATUS_REDIS', c.redis_host)
        c.redis_port = os.getenv('PRAELATUS_REDIS_PORT', c.redis_port)
        c.redis_password = os.getenv('PRAELATUS_REDIS_PASS')
        c.data_dir = os.getenv('PRAELATUS_DATA_DIRECTORY', c.data_dir)
        c.mq_server = os.getenv('PRAELATUS_MQ_SERVER', c.mq_server)
        c.instance_name = os.getenv('PRAELATUS_INSTANCE_NAME', c.instance_name)
        c.email_address = os.getenv('PRAELATUS_EMAIL_ADDRESS', c.email_address)
        c.smtp_server = os.getenv('PRAELATUS_SMTP_SERVER', c.smtp_server)
        c.smtp_password = os.getenv('PRAELATUS_SMTP_PASSWORD', c.smtp_password)

        return c


global config
config = Config().load()
