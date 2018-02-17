from os.path import join

from django.conf import settings
from django.core.management.base import BaseCommand

import yaml


class Command(BaseCommand):
    help = 'Generate the default minimal config.'

    def handle(self, *args, **kwargs):
        with open(join(settings.DATA_DIR, 'config.yaml'), 'w') as f:
            yaml.dump(settings.CONFIG, f, width=80, indent=4,
                      default_flow_style=False)
