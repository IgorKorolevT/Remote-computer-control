from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from chat.models import Computer


# Create your views here.
@login_required
def chat(request: HttpRequest) -> HttpResponse:
    user = request.user

    context = {
        "computers": user.computers.all(),
    }
    return render(request, "chat/chat.html", context)


@login_required
def chat_computer(request: HttpRequest, name) -> HttpResponse:
    user = request.user
    computers = user.computers.all()
    sent_m = user.sent_messages.all()
    received_m = user.received_messages.all()
    context = {
        "computers": computers,
        "chosen_computer": computers.get(name=name),
        "sent_m": sent_m,
        "received_m": received_m,
    }
    return render(request, "chat/chat_computer.html", context)


@login_required
def chat_room(request):
    computers = request.user.computers.all()
    context = {
        "computers": computers,
    }
    return render(request, "chat/chat.html", context)
