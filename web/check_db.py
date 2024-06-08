from django.conf import settings

if __name__ == '__main__':
    engine = settings.DATABASES['default']['ENGINE']
    print(engine)
