from django.db import models
from django.db.models.signals import pre_save
from LinkShortener.utils import LinkChecker,SlugGenerator

class URL(models.Model):
    Title = models.CharField(max_length=1000)
    Link = models.CharField(max_length=1000000, validators=[LinkChecker])
    Slug = models.SlugField(blank=True)
    Views = models.IntegerField(default=0)

    class Meta:
        ordering = ['Title']

    def __str__(self):
        return self.Title

def Links_presave(sender,instance,*args,**kwargs):
    if instance.Slug == '':
        STATUS = True
        while STATUS:
            SLUG = SlugGenerator()
            if not URL.objects.filter(Slug=SLUG).exists():
                instance.Slug = SLUG
                STATUS = False

pre_save.connect(Links_presave,sender=URL)