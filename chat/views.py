from typing import Dict, Union

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from computer.models import Computer
from chat.utils import computer_context, SenderTypes
from user.models import User


# Create your views here.
def get_base_context(user: User) -> Dict[str, Union[Computer, User]]:
    """Generate base context
    return {"computers": ...,}"""
    computers = user.computers.all()
    context = {"computers": computers, **SenderTypes.context()}
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
    computers = context["computers"]
    chosen_computer = get_object_or_404(computers, name=name)
    context_m = computer_context(user, chosen_computer)
    context.update(context_m)
    return render(request, "chat/chat_computer.html", context)
