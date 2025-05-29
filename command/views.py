from django.views.generic import ListView, DetailView, CreateView

from command.models import Command


# Create your views here.
class CommandListView(ListView):
    model = Command


class CommandDetailView(DetailView):
    model = Command
    queryset = Command.objects.select_related('author')

# class CommandCreateView(CreateView):
#     model = Command
