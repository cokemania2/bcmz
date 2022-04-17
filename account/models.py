from django.utils import timezone

from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)


class Token(models.Model):
    phone_number = models.CharField(
        max_length=15, unique=True)
    token = models.CharField(max_length=100, null=True)
    created_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    auth_num = models.IntegerField(null=True)
    accepted = models.BooleanField(default=False)


@receiver(post_save, sender=Token)
def delete_expire_token(sender, instance, created, **kwargs):
    Token.objects.filter(
        finish_time__lte=timezone.now(),
        accepted=False
    ).delete()
