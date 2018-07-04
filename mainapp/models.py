from django.db import models
import hashlib
import os


class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    m = hashlib.md5()
    m.update(filename.encode("UTF-8"))
    res = m.hexdigest()
    return "{}/{}/{}/{}".format(res[:2], res[2:4], res[4:6], res[6:]) + file_extension


class Article(models.Model):

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to=get_image_filename ,blank=True)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{0}/{1}'.format(self.category.name or 'uncategory', self.title)
