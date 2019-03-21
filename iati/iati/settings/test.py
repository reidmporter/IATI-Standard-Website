"""Settings for dev environments (overrides base settings)."""
import os
from django.utils.translation import gettext_lazy as _
from .base import *  # noqa: F401, F403 # pylint: disable=unused-wildcard-import, wildcard-import

ALLOWED_HOSTS = [
    "35.184.96.71",
    "35.184.226.236",
    "35.188.1.99",
    "35.188.73.34",
    "35.192.85.2",
    "35.192.136.167",
    "35.192.187.174",
    "35.193.7.13",
    "35.202.145.110",
    "35.224.112.202",
    "104.154.113.151",
    "104.154.120.187",
    "localhost",
]

SECRET_KEY = '-sg0o=f6(j3!4u6^86!j@0&l^3clslh-#f@02d2^p_4vy0ma0y'

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisci',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

USE_TZ = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media') # noqa

try:
    from .local import *  # # noqa: F401, F403  # pylint: disable=unused-wildcard-import, wildcard-import
except ImportError:
    pass
