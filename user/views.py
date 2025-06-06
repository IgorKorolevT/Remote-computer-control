from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from .forms import UserForm, UserUpdateForm


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
