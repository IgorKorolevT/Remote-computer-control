from typing import Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from chat.utils import computer_context, SenderTypes


# Create your views here.
def get_base_context(user: get_user_model()) -> Dict[str, QuerySet]:
    """Generate base context
    return {"computers": ...,}"""
    computers = user.computers.all()
    context = {"computer_list": computers, **SenderTypes.context()}
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
    computers = context["computer_list"]
    chosen_computer = get_object_or_404(computers, name=name)
    context_m = computer_context(user, chosen_computer)
    context.update(context_m)
    return render(request, "chat/chat_computer.html", context)
