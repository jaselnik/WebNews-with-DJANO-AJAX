import os

from ajax_web_news.settings.base import *

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir
)

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        'PASSWORD': 'password',
        "HOST": "db",
        "PORT": "5432",
    }
}

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static_in_dev"),)
