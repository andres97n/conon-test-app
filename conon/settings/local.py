
from .base import *
import json
import os

with open("secret/prod.json") as f:
    secret_local = json.loads(f.read())


def get_secret_local(secret_name, secrets=secret_local):
    try:
        return secrets[secret_name]
    except:
        msg = "La variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)


DEBUG = False

ALLOWED_HOSTS = ['*']


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
    "https://conon-app-test.herokuapp.com",
    "https://conon.netlify.app"
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://conon-app-test.herokuapp.com",
    "https://conon.netlify.app"
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [BASE_DIR / 'conon/../../static']

'''
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')
'''
