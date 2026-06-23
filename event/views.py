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
from .forms import ProgramCreateForm
from event.models import Program


class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    paginate_by = 25

    def get_queryset(self):
        return Program.objects.filter(user=self.request.user)


class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    queryset = Program.objects.select_related("user").prefetch_related("computers")

    def get_object(self, queryset=None):
        program = self.request.user.programs.filter(
            pk=self.kwargs.get("pk")
        ).select_related("user").prefetch_related("computers").first()

        if program is None:
            raise Http404()

        return program


class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    form_class = ProgramCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("program:detail", kwargs={"pk": self.object.pk})


class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = Program
    form_class = ProgramCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self) -> str:
        return reverse("program:detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None) -> Program:
        program = self.request.user.programs.filter(pk=self.kwargs.get("pk")).first()
        if program:
            return program
        raise Http404


class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    success_url = reverse_lazy("program:list")

    def get_object(self, queryset=None) -> Program:
        program = self.request.user.programs.filter(pk=self.kwargs.get("pk")).first()
        if program:
            return program
        raise Http404