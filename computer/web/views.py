import json
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from django.views.decorators.http import require_POST
from rest_framework.status import HTTP_502_BAD_GATEWAY

from computer.models import Computer
from computer.forms import ComputerAddForm, ComputerUpdateForm
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import logging


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
    return render(request, "computer/computer_add.html", {"form": form})


class ComputerDetailView(LoginRequiredMixin, DetailView):
    model = Computer

    def get_object(self, queryset=None) -> Computer:
        pk = (
            self.model.objects.filter(
                users__id=self.request.user.id, name=self.kwargs.get("name")
            )
            .prefetch_related("users")
            .first()
        )
        if pk:
            return pk
        raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_contex = self.get_task_context()
        context = self.get_context_data(object=self.object, is_monitoring=task_contex["is_monitoring"],
                                        every=task_contex["every"], period=task_contex["period"])
        return self.render_to_response(context)

    def get_task_context(self) -> dict[str, Any]:
        task_name = generate_same_name(self.request.user.id, self.object.name)
        try:
            task = PeriodicTask.objects.get(name=task_name)
            return {"is_monitoring": task.enabled, "every": task.interval.every, "period": task.interval.period}
        except PeriodicTask.DoesNotExist:
            # defaults
            return {"is_monitoring": False, "every": 5, "period": IntervalSchedule.MINUTES}  # TODO remove


class ComputerListView(LoginRequiredMixin, ListView):
    model = Computer

    def get_queryset(self):
        return self.model.objects.filter(users__id=self.request.user.id)


class ComputerUpdateView(LoginRequiredMixin, UpdateView):
    model = Computer
    form_class = ComputerUpdateForm

    def form_valid(self, form) -> HttpResponse:
        pk = self.model.objects.filter(
            users__id=self.request.user.id, name=self.kwargs.get("name")
        ).first()
        if pk:
            return super().form_valid(form)
        raise Http404

    def get_object(self, queryset=None) -> Computer:
        pk = self.model.objects.filter(
            users__id=self.request.user.id, name=self.kwargs.get("name")
        ).first()
        if pk:
            return pk
        raise Http404

    def get_success_url(self) -> str:
        return reverse("computer:detail", kwargs={"name": self.object.name})


class ComputerDeleteView(LoginRequiredMixin, DeleteView):
    model = Computer
    success_url = reverse_lazy("computer:list")

    def get_object(self, queryset=None) -> Computer:
        pk = self.model.objects.filter(
            users__id=self.request.user.id, name=self.kwargs.get("name")
        ).first()
        if pk:
            return pk
        raise Http404

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.users.remove(request.user)
        return HttpResponseRedirect(self.get_success_url())


# TODO remove
def generate_same_name(user_id: int, computer_name: str) -> str:
    return f"monitor_{user_id}_{computer_name}"


@login_required
@require_POST
def toggle_computer(request, name):
    logger = logging.getLogger(f"toggle_{name}")

    computer = get_object_or_404(Computer, name=name)
    user = request.user
    if user not in computer.users.all():
        logger.info(f"{user} don't have permission to change {computer.name} status")
        messages.error(request, "You don't have permission to change this computer's status.")
        return redirect('computer:list')

    is_on = request.POST.get('status') == 'On'
    logger.debug(f"is_on {is_on}")
    task_name = generate_same_name(user.id, computer.name)

    if is_on:
        every = int(request.POST.get('every'))
        get_period: str = request.POST.get('period').lower()
        period = None

        for period_choice in IntervalSchedule.PERIOD_CHOICES:
            if get_period in period_choice:
                period = period_choice[0]

        if period is None:
            raise Http404

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=every,
            period=period
        )

        PeriodicTask.objects.filter(name=task_name).delete() # delete old PeriodicTask with old IntervalSchedule

        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                'task': 'event.tasks.kill_programs_task',
                'interval': schedule,
                'args': json.dumps([user.id, computer.name]),
                'enabled': True,
                'description': f"Auto kill programs for user {user.id} on {computer.name}"
            }
        )

    else:
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.enabled = False
            task.save()
        except PeriodicTask.DoesNotExist:
            pass

    return redirect('computer:detail', name=computer.name)
