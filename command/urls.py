from django.urls import path
from . import views

app_name = "command"

urlpatterns = [
    path("", views.CommandListView.as_view(), name="list"),
    path("<int:pk>/", views.CommandDetailView.as_view(), name="detail"),
]
