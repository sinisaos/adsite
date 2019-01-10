from __future__ import unicode_literals
import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify

CATEGORY_CHOICES = (
    ('electronics', 'Electronics'),
    ('software', 'Software'),
    ('home', 'Home'),
    ('clothes', 'Clothes'),
    ('tools', 'Tools'),
    ('camping', 'Camping')
)


class Ad(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             editable=False)
    category = models.CharField(max_length=100,
                                choices=CATEGORY_CHOICES,
                                default='electronics')
    brand = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Ad, self).save(*args, **kwargs)


class Attachment(models.Model):
    ad = models.ForeignKey(Ad, related_name='images',
                           on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments')

    def delete(self):
        os.remove(self.file.path)
        return super(Attachment, self).delete()


class Rent(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
