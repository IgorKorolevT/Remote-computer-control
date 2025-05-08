from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserForm
from .models import User


# Create your views here.
def register_new_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user:home")
    else:
        form = UserForm()

    return render(request, "user/register_user.html", {"form": form})


class UserDetailView(generic.DetailView):
    model = User


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")
