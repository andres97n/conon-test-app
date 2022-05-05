
from .base import *
import json

with open("secret/prod.json") as f:
    secret_local = json.loads(f.read())


def get_secret_local(secret_name, secrets=secret_local):
    try:
        return secrets[secret_name]
    except:
        msg = "La variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret_local('DB_NAME'),
        'USER': get_secret_local('USER'),
        'PASSWORD': get_secret_local('PASSWORD'),
        'HOST': get_secret_local('HOST'),
        'PORT': get_secret_local('PORT'),
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']

'''
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')
'''
