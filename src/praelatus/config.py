"""Contains all of the configuration for Praelatus."""

import json
import os


class Config:
    """Contains all global app configuration and defaults."""

    default_db = 'postgres://postgres:postgres@localhost:5432/prae_dev'
    default_redis_host = 'localhost'
    default_redis_port = 6379
    default_redis_db = 0
    default_port = '8080'
    default_data_dir = './data'
    default_data_dir = './data/'
    default_mq_server = 'amqp://guest@localhost'
    default_smtp_server = 'localhost'
    default_email_address = 'praelatus@localhost'

    def __init__(self, **kwargs):
        """Build a new config."""
        self.db_url = kwargs.get('db_url', self.default_db)
        self.port = kwargs.get('port', self.default_port)
        self.redis_host = kwargs.get('redis_url', self.default_redis_host)
        self.redis_port = int(kwargs.get('redis_port', self.default_redis_port))  # noqa
        self.redis_db = int(kwargs.get('redis_db', self.default_redis_db))
        self.redis_password = kwargs.get('redis_password')
        self.data_dir = kwargs.get('data_dir', self.default_data_dir)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        self.mq_server = kwargs.get('mq_server', self.default_mq_server)
        self.smtp_server = kwargs.get('smtp_server', self.default_smtp_server)
        self.email_address = kwargs.get('email_address', self.default_email_address)

    def __repr__(self):
        """Return the str version of the internal dict."""
        return str(self.__dict__)

    def to_json(self):
        """Serialize the config to json."""
        return json.dumps(self.__dict__)

    def load(self):
        """Create a new Config based on the config file or environment variables."""  # noqa: E501
        if os.path.exists('/etc/praelatus/config.json'):
            config = json.loads('/etc/praelatus/config.json')
            return Config(**config)

        if os.path.exists('./config.json'):
            config = json.loads('./config.json')
            return Config(**config)

        config = {}
        config['db_url'] = os.environ.get('PRAELATUS_DB', self.default_db)
        config['port'] = os.environ.get('PRAELATUS_PORT', self.default_port)
        config['redis_url'] = os.getenv('PRAELATUS_REDIS', self.default_redis_host)
        config['redis_port'] = os.getenv('PRAELATUS_REDIS_PORT', self.default_redis_port)
        config['redis_password'] = os.getenv('PRAELATUS_REDIS_PASS')
        config['data_dir'] = os.getenv('PRAELATUS_DATA_DIRECTORY',
                                       self.default_data_dir)
        config['mq_server'] = os.getenv('PRAELATUS_MQ_SERVER',
                                        self.default_mq_server)

        return Config(**config)


global config
config = Config().load()
