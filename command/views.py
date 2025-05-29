from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import CommandCreatForm
from command.models import Command


# Create your views here.
class CommandListView(ListView):
    model = Command
    queryset = Command.objects.all().order_by('name')


class CommandDetailView(DetailView):
    model = Command
    queryset = Command.objects.select_related('author')

class CommandCreateView(CreateView):
    model = Command
    form_class = CommandCreatForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("command:detail", kwargs={"pk": self.object.pk})
