from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth import get_user_model


# Create your models here.
class Computer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField()
    users = models.ManyToManyField(get_user_model(), related_name="computers")
    channel_name = models.CharField(unique=True, null=True, blank=True)
    os = models.CharField(default="Windows")

    def __init__(self, *args, **kwargs):
        if kwargs.get("password"):
            kwargs["password"] = Computer.get_password(kwargs["password"])
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_password(raw_password: str) -> str:
        """Get hashed password"""
        return make_password(raw_password)

    def set_password(self, raw_password: str):
        """Set the password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verify the provided password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name}"
