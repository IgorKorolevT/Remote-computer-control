from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView

from computer.models import Computer
from computer.forms import ComputerAddForm




# Create your views here.
@login_required
def add_pk(
    request: HttpRequest,
) -> HttpResponse:
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
    return render(request, "computer/computer.html", {"form": form})


class ComputerDetailView(LoginRequiredMixin, DetailView):
    model = Computer
    queryset = Computer.objects.select_related("users")
