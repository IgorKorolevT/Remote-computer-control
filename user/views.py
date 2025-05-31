from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView

from chat.models import Computer
from .forms import UserForm, ComputerAddForm, UserUpdateForm


# Create your views here.

class UserCreateView(CreateView):
    form_class = UserForm
    model = get_user_model()
    template_name = "user/user_create.html"

    def get_success_url(self):
        if self.object:
            login(self.request, self.object)
            return reverse("user:profile")
        return reverse("user:register")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = get_user_model()
    success_url = reverse_lazy("user:profile")
    template_name = "user/user_update.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("user:register")

    def get_object(self, queryset=None):
        return self.request.user


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


@login_required
def add_pk(request: HttpRequest) -> HttpResponse:  # TODO: replace this func to more sunbelt place
    if request.method == "POST":
        form = ComputerAddForm(request.POST)
        if form.is_valid():
            try:
                pk = Computer.objects.get(name=form.cleaned_data["name"])
                if pk.check_password(form.cleaned_data["password"]):
                    pk.users.add(request.user)
                    return redirect(
                        "chat:chat_computers", name=form.cleaned_data["name"]
                    )
                messages.error(
                    request, "Invalid password of computer. Please try again."
                )
            except Computer.DoesNotExist:
                messages.error(request, "Invalid name of computer. Please try again.")
    else:
        form = ComputerAddForm()
    return render(request, "add/computer.html", {"form": form})
