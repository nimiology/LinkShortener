from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from Dashboard.utils import slug_generator


class ForgetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forgetPassword')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.user.username


def UserPreSave(sender, instance, *args, **kwargs):
    try:
        ForgetPassword.objects.get(user=instance)
    except ForgetPassword.DoesNotExist:
        ForgetPassword(user=instance, slug=slug_generator(ForgetPassword, 50, 150)).save()


post_save.connect(UserPreSave, sender=User)
