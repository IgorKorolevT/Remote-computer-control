from django.urls import reverse, reverse_lazy
from django.views import generic

from video.models import Video


# Create your views here.

class VideoListView(generic.ListView):
    model = Video


class VideoDetailView(generic.DetailView):
    model = Video


class VideoCreateView(generic.CreateView):
    model = Video
    fields = ["name", "description", "url", "preview"]

    def get_success_url(self):
        if self.object:
            return reverse("video:detail", kwargs={"pk": self.object.pk})
        return reverse("video:create")


class VideoUpdateView(generic.UpdateView):
    model = Video
    fields = ["name", "description", "url", "preview"]

    def get_success_url(self):
        if self.object:
            return reverse("video:detail", kwargs={"pk": self.object.pk})
        return reverse("video:update")


class VideoDeleteView(generic.DeleteView):
    model = Video
    success_url = reverse_lazy("video:list")
