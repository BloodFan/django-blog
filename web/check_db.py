import os

import django
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings_prod')
    django.setup()
    engine = settings.DATABASES['default']['ENGINE']
    print(engine)
