import subprocess
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    def run(self, *args, **options):
        subprocess.run('webpack')
        super(Command, self).run(*args, **options)
