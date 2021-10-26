from django.db import models
from django.db.models.signals import pre_save

from Dashboard.utils import slug_generator
from Dashboard.models import User


class URL(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='URLS')
    title = models.CharField(max_length=1024)
    link = models.URLField()
    slug = models.SlugField(blank=True, unique=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


def URLPreSave(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = slug_generator(URL, 5, 10)


pre_save.connect(URLPreSave, sender=URL)
