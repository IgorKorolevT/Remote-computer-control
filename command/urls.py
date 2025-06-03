from django.urls import path
from . import views

app_name = "command"

urlpatterns = [
    path("", views.CommandListView.as_view(), name="list"),
    path("<int:pk>/", views.CommandDetailView.as_view(), name="detail"),
    path("create/", views.CommandCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.CommandUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.CommandDeleteView.as_view(), name="delete"),
]
