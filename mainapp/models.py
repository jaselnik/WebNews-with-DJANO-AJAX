from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

import hashlib
import os


class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('main:category-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    m = hashlib.md5()
    m.update(filename.encode("UTF-8"))
    res = m.hexdigest()
    return "{}/{}/{}/{}".format(res[:2], res[2:4], res[4:6], res[6:]) + file_extension


class Article(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to=get_image_filename ,blank=True)
    content = models.TextField()

    comments = GenericRelation('comment')
    marks = GenericRelation('mark')

    def get_absolute_url(self):
        return reverse('main:article-detail', kwargs={'cat_slug': self.category.slug,
                                                      'slug': self.slug})

    def __str__(self):
        return '{0}/{1}'.format(self.category.name or 'uncategory', self.title)


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '{0}/{1}'.format(self.author.username, self.content[:10])


class Mark(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    MARK_CHOICES = (
        ('L', 'LIKE',),
        ('D', 'DISLIKE',),
    )
    status = models.CharField(max_length=7, choices=MARK_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '{0}/{1}'.format(self.status, self.author.username)


"""

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

class TaggedItem(models.Model):
    tag = models.SlugField()
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class Bookmark(models.Model):
    url = models.URLField()
    tags = GenericRelation(TaggedItem)

"""
