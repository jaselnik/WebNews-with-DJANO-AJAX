import os

from ajax_web_news.settings.base import *

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir
)

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ["ec2-3-17-60-80.us-east-2.compute.amazonaws.com"]

INSTALLED_APPS += ["django_pdb"]

MIDDLEWARE += [
    'django_pdb.middleware.PdbMiddleware',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ajax",
        "USER": "postgres",
        'PASSWORD': 'password',
        "HOST": "localhost",
        "PORT": "5432",
    }
}
