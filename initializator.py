import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core import management
from django.core.management import CommandError


def initialize():
    if not os.path.exists(f'{settings.BASE_DIR}/workflows/initialized.txt'):
        try:
            print('Initializing system...')

            # Initial admin user
            management.call_command(
                'createsuperuser',
                interactive=False,
                username='admin',
                email='admin@admin.admin'
            )
            user: User = User.objects.get(username='admin')
            user.set_password('admin')
            user.save()

            # Data seed
            seeds_directory: str = f'{settings.BASE_DIR}/seeds'

            for filename in os.listdir(seeds_directory):
                if filename.endswith('.json'):  # Ensure to only load JSON files
                    print("Loading: `%s`" % filename)
                    management.call_command('loaddata', os.path.join(seeds_directory, filename))
                    print("`%s` loaded!" % filename)

            with open(f'{settings.BASE_DIR}/workflows/initialized.txt', 'w') as file:
                file.write('Initialized')

            print('System initialized!')
        except CommandError:
            print(
                'Failed initialization! '
                'Probably database already contains entry/entries that should be initialized and/or '
                'initialized.txt is deleted after initialization.'
            )
