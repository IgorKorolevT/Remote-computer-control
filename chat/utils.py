from datetime import datetime
from typing import Union
from asgiref.sync import sync_to_async
from user.models import User
from chat.models import Computer, Room, Message
from django.db.models import QuerySet, Q
from typing import Dict

type UserComputer = Union[User, Computer]
type T_timestamp = Union[datetime, str]


def create_message(
    text: str,
    sender: UserComputer,
    recipient: UserComputer = None,
    room: Room = None,
    timestamp: T_timestamp = None,
) -> Message:
    """Create message.html and return it"""
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
    message.save()
    return message


def get_datetime(timestamp: T_timestamp) -> datetime:
    """Convert str to datetime or create datetime that need in fild timestamp"""
    if isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp)
    elif isinstance(timestamp, datetime):
        return timestamp
    elif timestamp is None:
        return datetime.now()
    else:
        raise TypeError


async def acreate_message(
    text: str,
    sender: UserComputer,
    recipient: UserComputer = None,
    recipient_room: Room = None,
    timestamp: T_timestamp = None,
) -> Message:
    """Create async message.html and return it"""
    message = await sync_to_async(create_message)(
        text, sender, recipient, recipient_room, timestamp
    )
    return message


def _m_computer(user: User, computer: Computer) -> QuerySet:
    """Return sent and received messages from computer"""
    messages = (
        Message.objects.filter(
            Q(sender_user=user, recipient_computer=computer)
            | Q(sender_computer=computer, recipient_user=user)
        )
        .select_related("sender_user", "sender_computer")
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
