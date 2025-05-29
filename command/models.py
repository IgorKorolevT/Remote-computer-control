from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Command(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    os = models.CharField()
    command = models.CharField()
    description = models.TextField(default="Not provided", null=True, blank=True)
    syntax = models.CharField(default="Not provided", blank=True)
    parameters = models.CharField(default="Not provided", blank=True)
    examples = models.TextField(default=None, null=True, blank=True)
    source = models.URLField(default=None, null=True, blank=True)
    # parent = models.ForeignKey('self', default=None, null=True, blank=True, related_name='children',
    #                            on_delete=models.SET_DEFAULT)
