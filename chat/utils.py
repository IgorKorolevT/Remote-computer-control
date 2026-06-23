import logging
import uuid
from datetime import datetime
from typing import Union
from user.models import User
from chat.models import Room, Message
from computer.models import Computer
from django.db.models import QuerySet, Q
from typing import Dict
from django.utils import timezone
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

type User_or_Computer = Union[User, Computer]
type T_timestamp = Union[datetime, str]


async def create_message(
        text: str,
        sender: User_or_Computer,
        recipient: User_or_Computer = None,
        room: Room = None,
        timestamp: T_timestamp = None,
) -> Message:
    """
    Create message and return it

    Notes:
         - don't save it to db
    """
    sender_user, sender_computer, recipient_user, recipient_computer, recipient_room = (
        None,
        None,
        None,
        None,
        None,
    )

    if not room and not recipient:
        raise TypeError("You must specify a recipient or a room to send messages")

    if isinstance(sender, User):
        sender_user = sender
    elif isinstance(sender, Computer):
        sender_computer = sender

    if isinstance(room, Room):
        recipient_room = room
    elif isinstance(recipient, User):
        recipient_user = recipient
    elif isinstance(recipient, Computer):
        recipient_computer = recipient

    timestamp = get_datetime(timestamp)

    message = Message(
        text=text,
        timestamp=timestamp,
        sender_user=sender_user,
        sender_computer=sender_computer,
        room=recipient_room,
        recipient_user=recipient_user,
        recipient_computer=recipient_computer,
    )

    return message


def get_datetime(timestamp: T_timestamp) -> datetime:
    """Convert str to datetime or create datetime that need in fild timestamp"""
    if isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp)
    elif isinstance(timestamp, datetime):
        return timestamp
    elif timestamp is None:
        return timezone.now()
    else:
        raise TypeError


# TODO rename
async def acreate_message(
        text: str,
        sender: User_or_Computer,
        recipient: User_or_Computer = None,
        recipient_room: Room = None,
        timestamp: T_timestamp = None,
) -> Message:
    """Create/Save async message and return it"""
    message = await create_message(
        text, sender, recipient, recipient_room, timestamp
    )
    await message.asave()
    return message


def _m_computer(user: User, computer: Computer) -> QuerySet:
    """Return sent and received messages from computer"""
    messages = (
        Message.objects.filter(
            Q(sender_user=user, recipient_computer=computer)
            | Q(sender_computer=computer, recipient_user=user)
        )
        .select_related("sender_user", "sender_computer")
        .only(
            "sender_user__username",
            "sender_computer__name",
            "timestamp",
            "text",
            "sender_computer__nickname",
        )
        .order_by("timestamp")
    )
    return messages


def computer_context(
        user: User, chosen_computer: Computer
) -> Dict[str, QuerySet | User]:
    """Get sent and received messages from chosen_computer. And return context dict"""
    if not isinstance(chosen_computer, Computer):
        raise TypeError("computer must be type Computer")

    messages = _m_computer(user, chosen_computer)
    context = {
        "chosen_computer": chosen_computer,
        "notifications": messages,
    }
    return context


class SenderTypes:
    USER = "user"
    COMPUTER = "computer"
    SYSTEM = "system"

    @staticmethod
    def context() -> Dict[str, str]:
        return {"User": SenderTypes.USER, "Computer": SenderTypes.COMPUTER, "System": SenderTypes.SYSTEM}


User = get_user_model()  # for typing, can make TYPE
logger_send_message_to_computer = logging.getLogger(__name__ + ".send_message_to_computer")


async def send_message_to_computer(user_id: int, computer_name: str, text: str, is_create_message: bool = True):
    """
    Send message to computer from system.
    If it online otherwise do nothing

    Can choose save message to db or not
    """

    try:
        user = await User.objects.aget(pk=user_id)

        computer = await Computer.objects.aget(name=computer_name)
        if not computer.channel_name:
            logger_send_message_to_computer.warning(f"computer {computer.name} doesn't have channel_name")
            return

        channel_layer = get_channel_layer()

        reply_channel = await channel_layer.new_channel(prefix="reply")

        # create message only if it needs
        if is_create_message:
            message = await acreate_message(text, user, computer)
        else:
            message = await create_message(text, user, computer)

        correlation_id = str(uuid.uuid4())

        await channel_layer.send(
            computer.channel_name,
            {
                "type_sender": SenderTypes.SYSTEM,
                "type": "pk_system_message",
                "message": message.text,
                "sender": int(user.id),
                "date": message.get_timestamp,
                "reply_to": reply_channel,
                "correlation_id": correlation_id
            }
        )

        response = await channel_layer.receive(reply_channel)

        if response.get("correlation_id") != correlation_id:
            # TODO do something
            raise ValueError(f"Correlation id isn't same {response.get("correlation_id")}-{correlation_id}")

        return response
    except Computer.DoesNotExist as e:
        logger_send_message_to_computer.error(e)
    except User.DoesNotExist as e:
        logger_send_message_to_computer.error(e)
