from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

<<<<<<< HEAD

=======
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
from mainapp.models import get_image_filename


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
<<<<<<< HEAD
    city = models.CharField(max_length=100, default='', blank=True, null=True)
    website = models.URLField(default='', blank=True, null=True)
    phone = models.IntegerField(default=0, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_image_filename, blank=True, null=True)

    def __str__(self):
        return self.user.username
=======
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=get_image_filename, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
