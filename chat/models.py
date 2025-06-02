import uuid
from django.db import models
from django.contrib.auth import get_user_model
from computer.models import Computer


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(get_user_model(), related_name="rooms", blank=True)
    computers = models.ManyToManyField(Computer, related_name="rooms", blank=True)

    def __str__(self):
        return f"name: {self.name}, slug: {self.slug}"


class Message(models.Model):
    FORMAT = "%B %d, %Y, %I:%M %p"
    text = models.TextField(max_length=500)  # change max_length
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_user = models.ForeignKey(
        get_user_model(),
        related_name="sent_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sender_computer = models.ForeignKey(
        Computer,
        related_name="sent_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        Room, related_name="messages", on_delete=models.CASCADE, null=True, blank=True
    )
    recipient_user = models.ForeignKey(
        get_user_model(),
        related_name="received_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recipient_computer = models.ForeignKey(
        Computer,
        related_name="received_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        sender = self.get_sender
        recipient = self.get_recipient
        return f"{sender} - {recipient}: {self.text[:20]}"

    @property
    def get_sender(self):
        sender = self.sender_user if self.sender_user else self.sender_computer
        return sender

    @property
    def get_recipient(self):
        recipient = (
            self.recipient_user if self.recipient_user else self.recipient_computer
        )
        return recipient

    @property
    def get_timestamp(self):
        str_t = self.timestamp.strftime(Message.FORMAT)
        return str_t
