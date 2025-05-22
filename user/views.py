from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from chat.models import Computer
from .forms import UserForm, ComputerAddForm, UserUpdateForm


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


@login_required()
def user_update(request: HttpRequest) -> HttpResponse:
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    if user_form.is_valid():
        user_form.save()
        messages.success(request, "Your account has been updated!")
        return redirect("user:profile")
    return render(request, "user/user_update.html", {"form": user_form})


class UserDeleteView(DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return self.request.user
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


@login_required
def add_pk(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ComputerAddForm(request.POST)
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
        form = ComputerAddForm()
    return render(request, "add/computer.html", {"form": form})
