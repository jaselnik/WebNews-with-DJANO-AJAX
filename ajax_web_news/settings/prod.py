from ajax_web_news.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        # 'PASSWORD': 'password',
        "HOST": "db",
        "PORT": "5432",
    }
}
