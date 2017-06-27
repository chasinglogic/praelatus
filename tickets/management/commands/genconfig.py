from os.path import join
from socket import gethostname

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate the default minimal config.'

    def handle(self, *args, **kwargs):
        config = {
            'mq_server': settings.CELERY_BROKER_URL,
            'allowed_hosts': [gethostname()],
            'media_root': settings.MEDIA_ROOT,
            'static_root': settings.STATIC_ROOT,
            'language_code': settings.LANGUAGE_CODE,
            'cache': settings.CACHES,
            'database': settings.DATABASES,
            'email': {
                'host': settings.EMAIL_HOST,
                'port': settings.EMAIL_PORT,
                'username': settings.EMAIL_HOST_USER,
                'password': settings.EMAIL_HOST_PASS,
                'use_tls': settings.EMAIL_USE_TLS,
                'use_ssl': settings.EMAIL_USE_SSL
            }
        }

        with open(join(settings.DATA_DIR, 'config.yaml'), 'w') as f:
            yaml.dump(config, f, width=80, indent=4, default_flow_style=False)
