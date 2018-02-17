from os import getenv
from os.path import abspath, dirname, join
from socket import gethostname

CONFIG = {
    'https': ('true' == getenv('PRAE_HTTPS_ENABLED', 'false').lower()),
    'debug': ('true' == getenv('PRAE_DEBUG', 'false').lower()),
    'allowed_hosts': getenv(
        'PRAE_ALLOWED_HOSTS',
        gethostname() + ',' + 'localhost'
    ).replace('"', '').split(','),
    'session_engine': getenv('PRAE_SESSION_ENGINE',
                             'django.contrib.sessions.backends.cached_db'),
    'database': {
        'default': {
            'ENGINE': getenv('PRAE_DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': getenv('PRAE_DB_NAME', 'praelatus'),
            'USER': getenv('PRAE_DB_USER', 'postgres'),
            'PASSWORD': getenv('PRAE_DB_PASS', 'postgres'),
            'HOST': getenv('PRAE_DB_HOST', '127.0.0.1'),
            'PORT': getenv('PRAE_DB_PORT', '5432')
        }
    },
    'language_code': getenv('PRAE_LANG_CODE', 'en-us'),
    'time_zone': getenv('PRAE_TZ', 'UTC'),
    'use_tz': bool(getenv('PRAE_USE_TZ', 'true')),
    'use_i18n': bool(getenv('PRAE_ENBALE_INTERNATIONALIZATION', 'true')),
    'cache': {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': getenv('PRAE_REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'KEY_PREFIX': 'PRAE',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            }
        }
    },
    'mq_server': getenv('PRAE_MQ_SERVER', 'amqp://guest:guest@localhost:5672//'),
    'mq_result_backend': getenv('PRAE_MQ_RESULT', 'rpc://'),
    'email': {
        'backend': getenv('PRAE_EMAIL_BACKEND',
                          'django.core.mail.backends.smtp.EmailBackend'),
        'address': getenv('PRAE_EMAIL_ADDRESS', 'praelatus@' + gethostname()),
        'host': getenv('PRAE_EMAIL_HOST', 'localhost'),
        'port': int(getenv('PRAE_EMAIL_PORT', '25')),
        'user': getenv('PRAE_EMAIL_USER', None),
        'pass': getenv('PRAE_EMAIL_PASS', None),
        'use_tls': ('true' == getenv('PRAE_EMAIL_USE_TLS', 'false').lower()),
        'use_ssl': ('true' == getenv('PRAE_EMAIL_USE_TLS', 'false').lower()),
    }
}
