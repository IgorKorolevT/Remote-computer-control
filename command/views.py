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
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity


# Create your views here.
class CommandListView(ListView):
    model = Command
    paginate_by = 25

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            return Command.objects.annotate(similarity=TrigramSimilarity("name", search)).filter(
                similarity__gt=0.025).order_by('-similarity')
        return Command.objects.all()


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
