from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from mainapp.models import get_image_filename


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=get_image_filename, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
