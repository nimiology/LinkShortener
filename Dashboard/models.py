from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
from Dashboard.utils import slug_genrator


class USER(models.Model):
    NAME = models.CharField(max_length=1024)
    USERNAME = models.CharField(max_length=1024)
    EMAIL = models.CharField(max_length=2048)
    PASSWORD = models.CharField(max_length=1024)
    Slug = models.SlugField(unique=True,blank=True)
    PasswordForget = models.SlugField(unique=True)
    Change = models.BooleanField(default=True)

    def __str__(self):
        return self.NAME


def USER_presave(sender,instance,*args,**kwargs):
    if not instance.Change:
        user = get_user_model()
        user.objects.create_user(username=instance.USERNAME,email=instance.EMAIL,password=instance.PASSWORD)
        instance.Change = True
    else:
        user = User.objects.get(email=instance.EMAIL)
        user.username = instance.USERNAME
        user.set_password(instance.PASSWORD)
    #forget password
    status = True
    while status:
        SLUG = slug_genrator()
        qs = USER.objects.filter(PasswordForget=SLUG)
        if not qs.exists():
            instance.PasswordForget = SLUG
            status = False
    #slug
    instance.Slug = instance.USERNAME


pre_save.connect(USER_presave,sender=USER)