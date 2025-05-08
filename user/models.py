from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    channel_name = models.CharField(unique=True, null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)
