import uuid

from django.db import models
from user.models import User


# Create your models here.
class Computer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField()
    users = models.ManyToManyField(User, related_name='computers')
    channel_name = models.CharField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"



class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='rooms', blank=True)
    computers = models.ManyToManyField(Computer, related_name='rooms', blank=True)

    def __str__(self):
        return f"name: {self.name}, slug: {self.slug}"


class Message(models.Model):
    text = models.TextField(max_length=500)  # change max_length
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, null=True, blank=True)
    sender_computer = models.ForeignKey(Computer, related_name='sent_messages', on_delete=models.CASCADE, null=True,
                                        blank=True)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    recipient_user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True,
                                       blank=True)
    recipient_computer = models.ForeignKey(Computer, related_name='received_messages', on_delete=models.CASCADE,
                                           null=True, blank=True)

    def __str__(self):
        sender = self.get_sender()
        recipient = self.get_recipient()
        return f'{sender} - {recipient}: {self.context[:20]}'

    def get_sender(self):
        sender = self.sender_user if self.sender_user else self.sender_computer
        return sender

    def get_recipient(self):
        recipient = self.recipient_user if self.recipient_user else self.recipient_computer
        return recipient
