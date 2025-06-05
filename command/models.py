from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Command(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='commands')
    name = models.CharField(unique=True)
    os = models.CharField()
    command = models.CharField()
    description = models.TextField(default="Not provided", null=True, blank=True)
    syntax = models.CharField(default="Not provided", blank=True)
    examples = ArrayField(models.CharField(max_length=200), default=list, null=True, blank=True)
    source = models.URLField(default=None, null=True, blank=True)
    parent = models.ForeignKey('self', default=None, null=True, blank=True, related_name='subcommands',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    parameter_name = models.CharField()
    description = models.TextField(default="Not provided", null=True, blank=True)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='parameters')
