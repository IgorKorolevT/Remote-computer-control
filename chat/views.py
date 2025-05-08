from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from user.models import User


# Create your views here.
def get_base_context(user: User) -> dict[str, Any]:
    """Generate base context
     return {"computers": ...,"friends": ...}"""
    computers = user.computers.all()
    friends = user.friends.all()
    context = {
        "computers": computers,
        "friends": friends
    }
    return context


@login_required
def chat(request: HttpRequest) -> HttpResponse:
    user = request.user

    context = get_base_context(user)
    return render(request, "chat/chat.html", context)


@login_required
def chat_computer(request: HttpRequest, name: str) -> HttpResponse:
    user = request.user
    context = get_base_context(user)
    sent_m = user.sent_messages.all() # TODO: user.sent_messages.all() not correct received
    received_m = user.received_messages.all() # TODO: user.received_messages.all() not correct sender
    chosen_computer = get_object_or_404(user.computers, name=name)
    context.update({
        "chosen_computer": chosen_computer,
        "sent_m": sent_m,
        "received_m": received_m,
    })
    return render(request, "chat/chat_computer.html", context)


@login_required
def chat_friend(request, username: str) -> HttpResponse:
    user = request.user
    context = get_base_context(user)
    chosen_friend = get_object_or_404(user.friends, username=username)
    context.update({
        "chosen_friend": chosen_friend,
    })
    return render(request, "chat/chat_friend.html", context)
