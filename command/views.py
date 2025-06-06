from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import CommandCreatForm
from command.models import Command


# Create your views here.
class CommandListView(ListView):
    model = Command
    queryset = Command.objects.all().order_by("name")
    paginate_by = 25


class CommandDetailView(DetailView):
    model = Command
    queryset = Command.objects.select_related("author").prefetch_related("parameters")


class CommandCreateView(LoginRequiredMixin, CreateView):
    model = Command
    form_class = CommandCreatForm

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("command:detail", kwargs={"pk": self.object.pk})


class CommandUpdateView(LoginRequiredMixin, UpdateView):
    model = Command
    form_class = CommandCreatForm

    def get_success_url(self) -> str:
        return reverse("command:detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None) -> Command:
        command = self.request.user.commands.filter(pk=self.kwargs.get("pk")).first()
        if command:
            return command
        raise Http404


class CommandDeleteView(LoginRequiredMixin, DeleteView):
    model = Command
    success_url = reverse_lazy("command:list")

    def get_object(self, queryset=None) -> Command:
        command = self.request.user.commands.filter(pk=self.kwargs.get("pk")).first()
        if command:
            return command
        raise Http404
