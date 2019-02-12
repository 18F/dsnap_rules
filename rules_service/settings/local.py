# flake8: noqa
from .base import *
import dj_database_url


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Just a simple secret key for development'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

WHITENOISE_AUTOREFRESH = True

if not DATABASES['default']:
    DATABASES['default'] = dj_database_url.parse(
        'postgres:///dsnap', conn_max_age=600)
