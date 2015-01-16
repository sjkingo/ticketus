from django.core import management
from django.core.management.base import BaseCommand

local_settings_module = 'ticketus_settings.local_settings'

class Command(BaseCommand):
    help = 'Initialises the database and sets up Ticketus'

    def handle(self, *args, **options):
        def _call(cmd, interactive=False):
            management.call_command(cmd, interactive=interactive, verbosity=0)

        # Look for the local_settings.py file
        try:
            __import__(local_settings_module)
        except ImportError:
            self.stderr.write('Error: Settings could not be found at {}. ' \
                    'Please properly configure settings first.'.format(local_settings_module))
            import sys
            sys.exit(1)

        _call('migrate')
        _call('collectstatic')
        self.stdout.write('Database configured successfully.')

        r = input('Do you wish to create a superuser that allows full access to the ticketing system? [y/n] ')
        if r == 'y':
            _call('createsuperuser', interactive=True)

        self.stdout.write('')
        self.stdout.write('Ticketus is now configured and ready to use.')
        self.stdout.write('You may point your WSGI server to `ticketus.wsgi`.')
        self.stdout.write('')
        self.stdout.write('Alternatively you may run the development server by')
        self.stdout.write('running `ticketus-admin runserver`')
