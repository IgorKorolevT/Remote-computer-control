from django.db import models
from user.models import User


# Create your models here.
class Computer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100)
    password = models.CharField()
    users = models.ManyToManyField(User, related_name='computers')
