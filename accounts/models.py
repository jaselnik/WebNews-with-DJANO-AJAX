from django.conf import settings
from django.db import models

from mainapp.models import get_image_filename


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default="", blank=True, null=True)
    website = models.URLField(default="", blank=True, null=True)
    phone = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_image_filename, blank=True, null=True)

    def __str__(self):
        return self.user.username
