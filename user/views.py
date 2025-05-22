from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from chat.models import Computer
from .forms import UserForm, ContactForm
from .models import User


# Create your views here.
def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user:home")
    else:
        form = UserForm()

    return render(request, "user/register_user.html", {"form": form})

@login_required()
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "user/profile.html")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

@login_required
def add_pk(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                pk = Computer.objects.get(name=form.cleaned_data["name"])
                if pk.check_password(form.cleaned_data["password"]):
                    pk.users.add(request.user)
                    return redirect("chat:chat_computers", name=form.cleaned_data["name"])
                messages.error(request, "Invalid password of computer. Please try again.")
            except Computer.DoesNotExist:
                messages.error(request, "Invalid name of computer. Please try again.")
    else:
        form = ContactForm()
    return render(request, "add/computer.html", {"form": form})
