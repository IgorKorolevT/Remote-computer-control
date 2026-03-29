from django.db import models
from computer.models import Computer
from django.contrib.auth import get_user_model

class Program(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="programs"
    )
    computers = models.ManyToManyField(Computer, related_name="programs")

    def __str__(self):
        return self.name