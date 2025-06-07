from django.urls import path
from video import views

app_name = "video"

urlpatterns = [
    path("", views.VideoListView.as_view(), name="list"),
    path("create/", views.VideoCreateView.as_view(), name="create"),
    path("<int:pk>/", views.VideoDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.VideoUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.VideoDeleteView.as_view(), name="delete"),
]
