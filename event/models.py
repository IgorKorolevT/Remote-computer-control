from django.db import models
from computer.models import Computer

class Program(models.Model):
    name = models.CharField(max_length=200, unique=True)
    computers = models.ManyToManyField(Computer, related_name="programs")

    def __str__(self):
        return self.name